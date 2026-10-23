"""Validação estrutural local; não verifica comportamento de agentes ou acesso ao CRM."""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
STATES = {"documentado", "parcial", "implementado", "validado", "não_verificado"}
INVENTORY = "docs/estado/ESTADO_DA_SKILL.json"
ENTRIES = (
    "skills/kommo-strategic-automation-architect/SKILL.md",
    "skills/kommo-strategic-automation-architect-agentes-ia/SKILL.md",
)
REQUIRED_FILES = (
    "README.md", "ARCHITECTURE.md", "SOURCE_REGISTER.md", "LICENSE", "AGENTS.md",
    "docs/relatorios-codex/README.md", "docs/relatorios-codex/ULTIMO_RELATORIO.md",
    "docs/estado/ESTADO_DA_SKILL.json", ".github/workflows/governanca.yml",
    ".github/workflows/validar-governanca.yml", "scripts/validar_governanca.py",
    "scripts/validar_diff_pr.py", "tests/test_validar_governanca.py",
    "tests/test_ci_governanca.py", "tests/test_validar_diff_pr.py",
)


def clean_markdown(text):
    return re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)


def anchors(text):
    result = set()
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", clean_markdown(text), re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        result.add(f"{slug}-{count}" if count else slug)
        counts[slug] = count + 1
    return result


def check_links(path, root):
    errors = []
    for raw in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", clean_markdown(path.read_text(encoding="utf-8"))):
        target = raw.strip()
        target = target[1:target.index(">")] if target.startswith("<") else target.split(' "', 1)[0]
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        destination = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        if not destination.is_relative_to(root.resolve()) or not destination.exists():
            errors.append(f"{path.relative_to(root)}: destino local ausente ou fora da raiz: {target}")
        elif url.fragment and destination.suffix == ".md":
            if unquote(url.fragment) not in anchors(destination.read_text(encoding="utf-8")):
                errors.append(f"{path.relative_to(root)}: âncora ausente: {target}")
    return errors


def check_inventory(data, root, warnings=None):
    warnings = warnings if warnings is not None else []
    errors = []
    if not isinstance(data, dict):
        return [f"{INVENTORY}: o conteúdo raiz deve ser um objeto JSON"]
    required = {"versao_esquema", "atualizado_em", "revisao_base", "modulos", "testes",
                "dependencias_externas", "limitacoes_conhecidas", "proximas_evolucoes"}
    if required - data.keys():
        return [f"{INVENTORY}: campos ausentes: {sorted(required - data.keys())}"]
    if data["versao_esquema"] != "1.0.0":
        errors.append(f"{INVENTORY}: versão de esquema desconhecida")
    if not isinstance(data["revisao_base"], str) or not re.fullmatch(r"[0-9a-f]{40}", data["revisao_base"]):
        errors.append(f"{INVENTORY}: revisão base deve ser hash Git completo")
    try:
        if not isinstance(data["atualizado_em"], str) or datetime.fromisoformat(data["atualizado_em"]).tzinfo is None:
            errors.append(f"{INVENTORY}: data sem fuso")
    except (TypeError, ValueError):
        errors.append(f"{INVENTORY}: data inválida")
    if not isinstance(data["modulos"], list):
        return errors + [f"{INVENTORY}: módulos deve ser uma lista"]
    for field, expected_type in (("testes", dict), ("dependencias_externas", list),
                                 ("limitacoes_conhecidas", list), ("proximas_evolucoes", list)):
        if not isinstance(data[field], expected_type):
            errors.append(f"{INVENTORY}: {field} deve ser {expected_type.__name__}")
    required_test_fields = {"ambiente", "cobertura", "estrutural", "integracao_kommo", "ci_remota"}
    if isinstance(data["testes"], dict) and required_test_fields - data["testes"].keys():
        errors.append(f"{INVENTORY}: campos de testes ausentes: {sorted(required_test_fields - data['testes'].keys())}")
    if not isinstance(data["dependencias_externas"], list):
        errors.append(f"{INVENTORY}: dependências externas deve ser uma lista")
    if not isinstance(data["proximas_evolucoes"], list):
        errors.append(f"{INVENTORY}: próximas evoluções deve ser uma lista")
    paths, ids, module_dependencies = [], [], []
    for module in data["modulos"]:
        if not isinstance(module, dict):
            errors.append(f"{INVENTORY}: módulo deve ser um objeto")
            continue
        fields = {"id", "caminho", "responsabilidade", "status_implementacao", "evidencias", "testes", "dependencias"}
        if fields - module.keys():
            errors.append(f"{INVENTORY}: módulo com campos obrigatórios ausentes")
            continue
        if not isinstance(module["id"], str) or not module["id"] or not isinstance(module["caminho"], str) or not module["caminho"]:
            errors.append(f"{INVENTORY}: id e caminho devem ser texto não vazio")
            continue
        paths.append(module["caminho"])
        ids.append(module["id"])
        if not isinstance(module["status_implementacao"], str) or module["status_implementacao"] not in STATES:
            errors.append(f"{INVENTORY}: estado inválido: {module['id']}")
        if not isinstance(module["dependencias"], list):
            errors.append(f"{INVENTORY}: dependências do módulo devem ser uma lista: {module['id']}")
        else:
            if any(not isinstance(item, str) or not item for item in module["dependencias"]):
                errors.append(f"{INVENTORY}: dependência sem identificador válido: {module['id']}")
            if len(module["dependencias"]) != len(set(item for item in module["dependencias"] if isinstance(item, str))):
                errors.append(f"{INVENTORY}: dependências duplicadas: {module['id']}")
            module_dependencies.extend((module["id"], item) for item in module["dependencias"] if isinstance(item, str))
        if not module["responsabilidade"] or not module["evidencias"] or not module["testes"]:
            errors.append(f"{INVENTORY}: módulo sem responsabilidade, evidência ou testes: {module['id']}")
        evidence_items = module["evidencias"]
        if not isinstance(evidence_items, list):
            errors.append(f"{INVENTORY}: evidências devem ser uma lista: {module['id']}")
            continue
        for item in [{"caminho": module["caminho"]}] + evidence_items:
            if not isinstance(item, dict) or not isinstance(item.get("caminho"), str):
                errors.append(f"{INVENTORY}: evidência sem caminho: {module['id']}")
                continue
            path = (root / item["caminho"]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.exists():
                errors.append(f"{INVENTORY}: caminho ausente ou fora da raiz: {item['caminho']}")
        if not isinstance(module["testes"], list):
            errors.append(f"{INVENTORY}: testes devem ser uma lista: {module['id']}")
            continue
        for test in module["testes"]:
            if not isinstance(test, dict) or not isinstance(test.get("status"), str) or test.get("status") not in STATES or not test.get("escopo") or not test.get("evidencia"):
                errors.append(f"{INVENTORY}: teste sem status, escopo ou evidência: {module['id']}")
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        errors.append(f"{INVENTORY}: módulos duplicados")
    expected = {p.relative_to(root).as_posix() for p in (root / "skills").rglob("*") if p.is_file()}
    expected.update(p.relative_to(root).as_posix() for p in (root / "Interface e Recursos do Kommo").rglob("*.md"))
    if expected - set(paths):
        errors.append(f"{INVENTORY}: módulos ausentes do inventário: {sorted(expected - set(paths))}")
    dependencies = data["dependencias_externas"]
    dependency_ids = []
    if isinstance(dependencies, list):
        for dependency in dependencies:
            if (not isinstance(dependency, dict) or not isinstance(dependency.get("id"), str)
                    or not dependency.get("id") or not isinstance(dependency.get("status"), str)
                    or dependency.get("status") not in STATES or not dependency.get("descricao")):
                errors.append(f"{INVENTORY}: dependência externa sem id, status ou descrição")
                continue
            dependency_ids.append(dependency["id"])
            if dependency["status"] == "não_verificado":
                warnings.append(f"Dependência externa {dependency['id']} está não_verificado; isso não reprova a validação estrutural.")
        if len(dependency_ids) != len(set(dependency_ids)):
            errors.append(f"{INVENTORY}: dependências externas duplicadas")
    known_references = set(ids) | set(dependency_ids)
    for module_id, dependency_id in module_dependencies:
        if dependency_id not in known_references:
            errors.append(f"{INVENTORY}: dependência sem referência correspondente: {module_id} -> {dependency_id}")
    evolutions = data["proximas_evolucoes"]
    if isinstance(evolutions, list) and len(evolutions) != 3:
        errors.append(f"{INVENTORY}: devem ser recomendadas três evoluções")
    if isinstance(evolutions, list):
        for evolution in evolutions:
            if not isinstance(evolution, dict) or not evolution.get("prioridade") or not evolution.get("evolucao") or not isinstance(evolution.get("criterios_aceitacao"), list) or not evolution["criterios_aceitacao"]:
                errors.append(f"{INVENTORY}: recomendação sem prioridade, descrição ou critérios de aceitação")
    return errors


def check_reports(root):
    folder = root / "docs/relatorios-codex"
    latest_path = folder / "ULTIMO_RELATORIO.md"
    if not latest_path.is_file():
        return ["docs/relatorios-codex/ULTIMO_RELATORIO.md: arquivo obrigatório ausente"]
    latest = latest_path.read_text(encoding="utf-8")
    match = re.match(r"Histórico: \[([^\]]+)\]\((historico/[^)]+\.md)\)\.\n\n", latest)
    if not match:
        return ["Último relatório sem referência histórica no formato esperado"]
    history = folder / match[2]
    if not history.resolve().is_relative_to((folder / "historico").resolve()) or not history.is_file():
        return ["Relatório histórico ausente ou fora do diretório"]
    original = history.read_text(encoding="utf-8")
    # A cópia está um nível acima do histórico; adapta apenas destinos de links.
    adapted = re.sub(r"(\]\()\.\./", r"\1", original)
    errors = []
    if latest[match.end():] != adapted:
        errors.append("docs/relatorios-codex/ULTIMO_RELATORIO.md: diverge do relatório histórico")
    execution_pattern = re.compile(r"^[ \t]*[-*]?\s*Execução:\s*([^,\r\n]+)", re.M)
    history_id = execution_pattern.search(original)
    latest_id = execution_pattern.search(latest)
    if (history_id or latest_id) and (not history_id or not latest_id or history_id.group(1) != latest_id.group(1)):
        errors.append("docs/relatorios-codex/ULTIMO_RELATORIO.md: identificador da execução diverge do histórico")
    sections = re.findall(r"^## (\d+)\. .+", original, re.M)
    if sections != [str(i) for i in range(1, 11)]:
        errors.append(f"{match[2]}: relatório deve conter dez seções numeradas em ordem")
    return errors


def validate(root=ROOT):
    errors = []
    warnings = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"{relative}: arquivo obrigatório ausente")
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode("utf-8").split("\0")
    # Os diretórios abaixo incluem arquivos novos antes do primeiro git add.
    markdown = {root / p for p in tracked if p.endswith(".md")}
    markdown.update((root / "docs").rglob("*.md"))
    markdown.add(root / "AGENTS.md")
    for path in sorted(markdown):
        if not path.is_file():
            errors.append(f"{path.relative_to(root)}: arquivo Markdown rastreado ausente")
            continue
        errors.extend(check_links(path, root))
    for entry in ENTRIES:
        if not (root / entry).is_file():
            errors.append(f"{entry}: ponto de entrada obrigatório ausente")
            continue
        text = (root / entry).read_text(encoding="utf-8")
        if not re.match(r"\A---\r?\nname: \S+\r?\ndescription: .+\r?\n---", text):
            errors.append(f"Entrada Agent Skills ilegível ou sem metadados esperados: {entry}")
    inventory_path = root / INVENTORY
    try:
        data = json.loads(inventory_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return errors + [f"{INVENTORY}: JSON inválido na linha {exc.lineno}, coluna {exc.colno}"], warnings, len(markdown), 0
    except OSError as exc:
        return errors + [f"{INVENTORY}: não foi possível ler o arquivo ({exc.strerror})"], warnings, len(markdown), 0
    errors.extend(check_inventory(data, root, warnings))
    errors.extend(check_reports(root))
    module_count = len(data["modulos"]) if isinstance(data, dict) and isinstance(data.get("modulos"), list) else 0
    return errors, warnings, len(markdown), module_count


if __name__ == "__main__":
    try:
        failures, warnings, markdown_count, module_count = validate()
    except OSError as exc:
        print(f"ERRO: {exc.filename or 'repositório'}: {exc.strerror or type(exc).__name__}")
        sys.exit(1)
    except (ValueError, KeyError, TypeError) as exc:
        print(f"ERRO: estrutura inválida ({type(exc).__name__})")
        sys.exit(1)
    for failure in failures:
        print(f"ERRO: {failure}")
    for warning in warnings:
        print(f"AVISO: {warning}")
    if not failures:
        print(f"OK: {markdown_count} Markdown; 2 entradas; {module_count} módulos; JSON e relatórios íntegros.")
    sys.exit(bool(failures))
