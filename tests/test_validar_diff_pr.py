"""Valida verificações locais do diff sem expor os valores sinalizados."""

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validar_diff_pr import find_secret_indicators, validate_diff


class PullRequestDiffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="validar-diff-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "--quiet")
        self.git("-c", "user.name=Validador", "-c", "user.email=validador@example.invalid", "commit", "--allow-empty", "-m", "base")
        self.base = self.git("rev-parse", "HEAD").stdout.decode().strip()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, check=True)

    def write_changed(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        self.git("add", "-N", path)

    def test_known_secret_shape_is_detected_without_returning_value(self):
        value = "ghp_" + "A" * 36
        findings = find_secret_indicators(f"token={value}")
        self.assertIn("token GitHub", findings)
        self.assertNotIn(value, str(findings))
        self.assertIn("token GitHub", find_secret_indicators(f"Example documentation: {value}"))

    def test_documentation_placeholders_are_not_secrets(self):
        value = "EXAMPLE_" + "A" * 36
        self.assertEqual(find_secret_indicators(f"api_key='{value}'"), [])

    def test_changed_python_syntax_is_checked_without_writing_bytecode(self):
        self.write_changed("roteiro com espaço.py", "if True print('inválido')\n")
        errors = validate_diff(self.base, self.root)
        self.assertTrue(any("roteiro com espaço.py:1" in error and "sintaxe Python inválida" in error for error in errors))
        self.assertFalse((self.root / "__pycache__").exists())

    def test_secret_in_added_line_is_reported_without_its_value(self):
        value = "A9_" + "xY" * 20
        self.write_changed("configuracao.md", f"kommo_access_token='{value}'\n")
        errors = validate_diff(self.base, self.root)
        self.assertTrue(any("configuracao.md:1" in error and "campo sensível" in error for error in errors))
        self.assertNotIn(value, "\n".join(errors))

    def test_invalid_base_reference_is_rejected_clearly(self):
        from scripts.validar_diff_pr import changed_paths

        with self.assertRaisesRegex(RuntimeError, "revisão base"):
            changed_paths("referencia-inexistente", self.root)


if __name__ == "__main__":
    unittest.main()
