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
ENTRIES = (
    "skills/kommo-strategic-automation-architect/SKILL.md",
    "skills/kommo-strategic-automation-architect-agentes-ia/SKILL.md",
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


def check_inventory(data, root):
    errors = []
    required = {"versao_esquema", "atualizado_em", "revisao_base", "modulos", "testes",
                "dependencias_externas", "limitacoes_conhecidas", "proximas_evolucoes"}
    if required - data.keys():
        return [f"Inventário: campos ausentes: {sorted(required - data.keys())}"]
    if data["versao_esquema"] != "1.0.0":
        errors.append("Versão de esquema desconhecida")
    if not re.fullmatch(r"[0-9a-f]{40}", data["revisao_base"]):
        errors.append("Revisão base deve ser hash Git completo")
    try:
        if datetime.fromisoformat(data["atualizado_em"]).tzinfo is None:
            errors.append("Data sem fuso")
    except ValueError:
        errors.append("Data inválida")
    paths, ids = [], []
    for module in data["modulos"]:
        fields = {"id", "caminho", "responsabilidade", "status_implementacao", "evidencias", "testes", "dependencias"}
        if fields - module.keys():
            errors.append("Módulo com campos obrigatórios ausentes")
            continue
        paths.append(module["caminho"])
        ids.append(module["id"])
        if module["status_implementacao"] not in STATES:
            errors.append(f"Estado inválido: {module['id']}")
        if not module["responsabilidade"] or not module["evidencias"] or not module["testes"]:
            errors.append(f"Módulo sem responsabilidade, evidência ou testes: {module['id']}")
        for item in [{"caminho": module["caminho"]}] + module["evidencias"]:
            path = (root / item["caminho"]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.exists():
                errors.append(f"Caminho de inventário ausente ou fora da raiz: {item['caminho']}")
        for test in module["testes"]:
            if test.get("status") not in STATES or not test.get("escopo") or not test.get("evidencia"):
                errors.append(f"Teste sem status, escopo ou evidência: {module['id']}")
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        errors.append("Módulos duplicados")
    expected = {p.relative_to(root).as_posix() for p in (root / "skills").rglob("*") if p.is_file()}
    expected.update(p.relative_to(root).as_posix() for p in (root / "Interface e Recursos do Kommo").rglob("*.md"))
    if expected - set(paths):
        errors.append(f"Módulos ausentes do inventário: {sorted(expected - set(paths))}")
    if len(data["proximas_evolucoes"]) != 3:
        errors.append("Inventário deve recomendar três evoluções")
    return errors


def check_reports(root):
    folder = root / "docs/relatorios-codex"
    latest = (folder / "ULTIMO_RELATORIO.md").read_text(encoding="utf-8")
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
        errors.append("Último relatório diverge do histórico")
    sections = re.findall(r"^## (\d+)\. .+", original, re.M)
    if sections != [str(i) for i in range(1, 11)]:
        errors.append("Relatório deve conter dez seções numeradas em ordem")
    return errors


def validate(root=ROOT):
    errors = []
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode("utf-8").split("\0")
    # Os diretórios abaixo incluem arquivos novos antes do primeiro git add.
    markdown = {root / p for p in tracked if p.endswith(".md")}
    markdown.update((root / "docs").rglob("*.md"))
    markdown.add(root / "AGENTS.md")
    for path in sorted(markdown):
        errors.extend(check_links(path, root))
    for entry in ENTRIES:
        text = (root / entry).read_text(encoding="utf-8")
        if not re.match(r"\A---\r?\nname: \S+\r?\ndescription: .+\r?\n---", text):
            errors.append(f"Entrada Agent Skills ilegível ou sem metadados esperados: {entry}")
    data = json.loads((root / "docs/estado/ESTADO_DA_SKILL.json").read_text(encoding="utf-8"))
    errors.extend(check_inventory(data, root))
    errors.extend(check_reports(root))
    return errors, len(markdown), len(data["modulos"])


if __name__ == "__main__":
    try:
        failures, markdown_count, module_count = validate()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FALHA: {exc}")
        sys.exit(1)
    for failure in failures:
        print(f"FALHA: {failure}")
    if not failures:
        print(f"OK: {markdown_count} Markdown; 2 entradas; {module_count} módulos; JSON e relatórios íntegros.")
    sys.exit(bool(failures))
