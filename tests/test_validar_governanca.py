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
            doc.write_text("[web](https://example.invalid)\n```md\n[exemplo](ausente.md)\n```\n", encoding="utf-8")
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
        self.assertEqual(check_inventory(data, ROOT), [])
        broken = copy.deepcopy(data)
        broken["modulos"].pop(0)
        self.assertTrue(any("ausentes do inventário" in e for e in check_inventory(broken, ROOT)))

    def test_inventory_rejects_invalid_status_and_missing_evidence_path(self):
        data = json.loads((ROOT / "docs/estado/ESTADO_DA_SKILL.json").read_text(encoding="utf-8"))
        data["modulos"][0]["status_implementacao"] = "aprovado"
        data["modulos"][0]["evidencias"][0]["caminho"] = "ausente.md"
        errors = check_inventory(data, ROOT)
        self.assertTrue(any("Estado inválido" in e for e in errors))
        self.assertTrue(any("Caminho de inventário" in e for e in errors))

    def test_reports_detect_divergence_and_missing_sections(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "docs/relatorios-codex"
            (folder / "historico").mkdir(parents=True)
            original = "\n".join(f"## {i}. Seção\nTexto.\n" for i in range(1, 11))
            (folder / "historico/teste.md").write_text(original, encoding="utf-8")
            latest = folder / "ULTIMO_RELATORIO.md"
            prefix = "Histórico: [Teste](historico/teste.md).\n\n"
            latest.write_text(prefix + original, encoding="utf-8")
            self.assertEqual(check_reports(root), [])
            latest.write_text(prefix + original + "Divergência", encoding="utf-8")
            self.assertIn("Último relatório diverge do histórico", check_reports(root))
            (folder / "historico/teste.md").write_text("## 1. Incompleto\n", encoding="utf-8")
            self.assertTrue(any("dez seções" in e for e in check_reports(root)))


if __name__ == "__main__":
    unittest.main()
