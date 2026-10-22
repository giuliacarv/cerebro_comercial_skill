"""Executa o validador real em cópias temporárias, com falhas deliberadas."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ValidationCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="governanca-ci-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        files = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8")
        for name in filter(None, files.split("\0")):
            source, target = ROOT / name, self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        self.git("init", "--quiet")
        self.git("-c", "core.autocrlf=false", "add", ".")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, check=True)

    def validate(self):
        return subprocess.run(
            [sys.executable, "scripts/validar_governanca.py"], cwd=self.root,
            capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

    def test_command_accepts_valid_repository(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK:", result.stdout)

    def test_command_rejects_broken_link(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[Link quebrado](arquivo-inexistente.md)\n")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("destino local ausente", result.stdout)

    def test_command_rejects_incomplete_inventory(self):
        path = self.root / "docs/estado/ESTADO_DA_SKILL.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["modulos"].pop(0)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ausentes do inventário", result.stdout)

    def test_command_rejects_divergent_report(self):
        with (self.root / "docs/relatorios-codex/ULTIMO_RELATORIO.md").open("a", encoding="utf-8") as stream:
            stream.write("\nAlteração sem atualização do histórico.\n")
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Último relatório diverge", result.stdout)

    def test_git_check_rejects_whitespace_in_committed_diff(self):
        # write-tree compara snapshots do índice sem criar commits ou usar identidade pessoal.
        before = self.git("write-tree").stdout.decode().strip()
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\nWhitespace deliberado.  \n")
        self.git("-c", "core.autocrlf=false", "add", "README.md")
        after = self.git("write-tree").stdout.decode().strip()
        result = subprocess.run(
            ["git", "diff", "--check", before, after], cwd=self.root, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"trailing whitespace", result.stdout)


if __name__ == "__main__":
    unittest.main()
