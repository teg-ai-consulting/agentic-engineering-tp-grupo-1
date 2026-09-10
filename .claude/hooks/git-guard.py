#!/usr/bin/env python3
"""PreToolUse / Bash — bloquea que un agente commitee o pushee a main.

Los devs trabajan en su worktree, en una rama. main solo se toca por PR + merge
humano. GOBERNANZA.md lo dice; este hook lo hace cumplir.
"""
import json
import re
import subprocess
import sys

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

# push directo a main
if re.search(r"\bgit\s+push\b", cmd) and re.search(r"\bmain\b", cmd):
    print("BLOQUEADO: push a main. Trabajá en tu rama/worktree y abrí un PR.", file=sys.stderr)
    sys.exit(2)

# commit estando parado en main
if re.search(r"\bgit\s+commit\b", cmd):
    try:
        rama = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        rama = ""
    if rama == "main":
        print("BLOQUEADO: commit en main. Creá una rama primero (git checkout -b ...).", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
