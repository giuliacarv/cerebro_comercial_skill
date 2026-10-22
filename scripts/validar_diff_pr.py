"""Valida sintaxe Python e sinais evidentes de segredo no diff de uma branch."""

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATTERNS = (
    ("token GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b")),
    ("chave AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("chave de API", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("chave privada", re.compile(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----")),
)
ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(?:api[_-]?(?:key|token)|access[_-]?token|refresh[_-]?token|"
    r"client[_-]?secret|kommo[_-]?(?:access[_-]?)?token|password|senha|secret)\b"
    r"\s*[:=]\s*[\"']?(?P<value>[A-Za-z0-9_./+=-]{24,})"
)
PLACEHOLDER_PREFIX = re.compile(
    r"(?i)^(?:your|example|sample|dummy|fake|test|placeholder|redacted|replace|changeme|todo|x{4,})(?:[_ .-]|$)"
)


def is_placeholder(value):
    normalized = value.strip("\"'`{}<> ").casefold()
    return bool(PLACEHOLDER_PREFIX.search(normalized)) or normalized in {
        "your_token_here", "your_secret_here", "replace_me", "insert_token", "insert_secret",
    }


def is_placeholder_token(value):
    prefixes = ("github_pat_", "ghp_", "gho_", "ghu_", "ghs_", "ghr_", "AKIA", "sk-proj-", "sk-", "eyJ")
    for prefix in prefixes:
        if value.startswith(prefix) and is_placeholder(value[len(prefix):]):
            return True
    return False


def find_secret_indicators(line):
    findings = []
    for label, pattern in TOKEN_PATTERNS:
        match = pattern.search(line)
        if match and not is_placeholder_token(match.group(0)):
            findings.append(label)
    assignment = ASSIGNMENT_PATTERN.search(line)
    if assignment and not is_placeholder(assignment.group("value")):
        findings.append("valor associado a campo sensível")
    return findings


def changed_paths(base, root=ROOT):
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "-z", base, "--"],
        cwd=root, capture_output=True,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"não foi possível comparar a revisão base ({message or 'git diff falhou'})")
    return [item.decode("utf-8", errors="replace") for item in result.stdout.split(b"\0") if item]


def check_python_syntax(paths, root=ROOT):
    errors = []
    for relative in paths:
        path = root / relative
        if path.suffix.lower() != ".py":
            continue
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=relative)
        except SyntaxError as exc:
            errors.append(f"{relative}:{exc.lineno}:{exc.offset}: sintaxe Python inválida ({exc.msg})")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{relative}: não foi possível ler o arquivo Python ({type(exc).__name__})")
    return errors


def check_added_lines(base, root=ROOT):
    result = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--unified=0", base, "--"],
        cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        message = result.stderr.strip()
        raise RuntimeError(f"não foi possível ler o diff da revisão base ({message or 'git diff falhou'})")
    findings = []
    current_path = None
    line_number = 0
    for line in result.stdout.splitlines():
        if line.startswith("+++ b/"):
            current_path = line[6:]
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            line_number = int(match.group(1)) - 1 if match else 0
        elif line.startswith("+") and not line.startswith("+++"):
            line_number += 1
            if current_path:
                for label in find_secret_indicators(line[1:]):
                    findings.append(f"{current_path}:{line_number}: possível {label}")
        elif line.startswith(" "):
            line_number += 1
    return findings


def validate_diff(base, root=ROOT):
    paths = changed_paths(base, root)
    errors = check_python_syntax(paths, root)
    errors.extend(check_added_lines(base, root))
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", help="commit ou referência da base para comparar com a árvore atual")
    args = parser.parse_args(argv)
    try:
        errors = validate_diff(args.base)
    except RuntimeError as exc:
        print(f"ERRO: {exc}")
        return 1
    for error in errors:
        print(f"ERRO: {error}")
    if errors:
        return 1
    print("OK: sintaxe Python alterada válida; nenhum segredo evidente no diff adicionado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
