"""Casos positivos e falhas deliberadas, sem rede nem dependências externas."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.validar_governanca import ROOT, anchors, check_inventory, check_links, check_reports


class GovernanceTests(unittest.TestCase):
    def test_links_detect_missing_target_and_anchor(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = root / "guia.md"
            doc.write_text("# Olá mundo\n[ok](#olá-mundo)\n[erro](ausente.md)\n[âncora](#inexistente)\n", encoding="utf-8")
            self.assertEqual(len(check_links(doc, root)), 2)

    def test_links_ignore_code_and_external_urls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = root / "guia.md"
            doc.write_text("[web](https://192.0.2.1/recurso)\n```md\n[exemplo](ausente.md)\n```\n", encoding="utf-8")
            self.assertEqual(check_links(doc, root), [])

    def test_links_support_spaces_url_encoding_and_fragments(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "guia com espaço.md"
            target.write_text("# Seção de ação\n", encoding="utf-8")
            doc = root / "indice.md"
            doc.write_text(
                "[literal](<guia com espaço.md#seção-de-ação>)\n"
                "[codificado](guia%20com%20espa%C3%A7o.md#se%C3%A7%C3%A3o-de-a%C3%A7%C3%A3o)\n",
                encoding="utf-8",
            )
            self.assertEqual(check_links(doc, root), [])

    def test_links_reject_escape_from_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = root / "guia.md"
            doc.write_text("[fora](../fora.md)\n", encoding="utf-8")
            self.assertEqual(len(check_links(doc, root)), 1)

    def test_duplicate_headings(self):
        self.assertEqual(anchors("# Seção\n# Seção\n"), {"seção", "seção-1"})

    def test_inventory_matches_real_structure(self):
        data = json.loads((ROOT / "docs/estado/ESTADO_DA_SKILL.json").read_text(encoding="utf-8"))
        warnings = []
        self.assertEqual(check_inventory(data, ROOT, warnings), [])
        self.assertTrue(any("kommo-crm" in warning and "não_verificado" in warning for warning in warnings))
        broken = copy.deepcopy(data)
        broken["modulos"].pop(0)
        self.assertTrue(any("ausentes do inventário" in e for e in check_inventory(broken, ROOT)))

    def test_inventory_rejects_invalid_status_and_missing_evidence_path(self):
        data = json.loads((ROOT / "docs/estado/ESTADO_DA_SKILL.json").read_text(encoding="utf-8"))
        data["modulos"][0]["status_implementacao"] = "aprovado"
        data["modulos"][0]["evidencias"][0]["caminho"] = "ausente.md"
        errors = check_inventory(data, ROOT)
        self.assertTrue(any("estado inválido" in e for e in errors))
        self.assertTrue(any("caminho ausente" in e for e in errors))

    def test_inventory_rejects_missing_module_path(self):
        data = json.loads((ROOT / "docs/estado/ESTADO_DA_SKILL.json").read_text(encoding="utf-8"))
        data["modulos"][0]["caminho"] = "arquivo-inexistente.md"
        self.assertTrue(any("caminho ausente" in error for error in check_inventory(data, ROOT)))

    def test_inventory_rejects_duplicate_module_references(self):
        data = json.loads((ROOT / "docs/estado/ESTADO_DA_SKILL.json").read_text(encoding="utf-8"))
        duplicate = copy.deepcopy(data["modulos"][0])
        data["modulos"].append(duplicate)
        self.assertTrue(any("módulos duplicados" in error for error in check_inventory(data, ROOT)))

    def test_inventory_rejects_unknown_module_dependency(self):
        data = json.loads((ROOT / "docs/estado/ESTADO_DA_SKILL.json").read_text(encoding="utf-8"))
        data["modulos"][0]["dependencias"].append("modulo-inexistente")
        self.assertTrue(any("dependência sem referência correspondente" in error for error in check_inventory(data, ROOT)))

    def test_reports_detect_divergence_and_missing_sections(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "docs/relatorios-codex"
            (folder / "historico").mkdir(parents=True)
            original = "Execução: TAREFA-TESTE, em 2026-10-22.\n\n" + "\n".join(
                f"## {i}. Seção\nTexto.\n" for i in range(1, 11)
            )
            (folder / "historico/teste.md").write_text(original, encoding="utf-8")
            latest = folder / "ULTIMO_RELATORIO.md"
            prefix = "Histórico: [Teste](historico/teste.md).\n\n"
            latest.write_text(prefix + original, encoding="utf-8")
            self.assertEqual(check_reports(root), [])
            latest.write_text(prefix + original + "Divergência", encoding="utf-8")
            self.assertTrue(any("diverge do relatório histórico" in error for error in check_reports(root)))
            latest.write_text(prefix + original.replace("TAREFA-TESTE", "TAREFA-DIVERGENTE"), encoding="utf-8")
            self.assertTrue(any("identificador da execução diverge" in error for error in check_reports(root)))
            (folder / "historico/teste.md").write_text("## 1. Incompleto\n", encoding="utf-8")
            self.assertTrue(any("dez seções" in e for e in check_reports(root)))


if __name__ == "__main__":
    unittest.main()
