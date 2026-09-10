#!/usr/bin/env python3
"""PostToolUse / Edit|Write — corre ruff sobre el .py recién tocado.

Si hay errores de lint, se los devuelve al agente para que corrija (bucle de
auto-corrección de la Clase 1). No bloquea nada; solo informa.
"""
import json
import shutil
import subprocess
import sys

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")

if not path.endswith(".py"):
    sys.exit(0)

if shutil.which("ruff") is None:
    sys.exit(0)  # sin ruff instalado, no molestamos

r = subprocess.run(["ruff", "check", path], capture_output=True, text=True)
if r.returncode != 0:
    print(f"ruff encontró problemas en {path}:\n{r.stdout}{r.stderr}", file=sys.stderr)
    sys.exit(2)  # exit 2 = feedback al agente

sys.exit(0)
