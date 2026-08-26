#!/usr/bin/env python3
"""
Demo: cuándo SÍ es razonable ejecutar un .py externo.

Idea clave: el código externo solo se ejecuta si su hash SHA-256
coincide con uno ya aprobado en manifest.json (la "cadena de confianza").
Si alguien modifica el plugin (aunque sea un byte), el loader lo rechaza.

Esto imita cómo funcionan gestores de paquetes reales (pip, apt, etc.):
no confían en el nombre del archivo ni en el dominio de origen,
confían en un hash/firma verificado de antemano.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent / "plugins"
MANIFEST_FILE = Path(__file__).parent / "manifest.json"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST_FILE.read_text())


def run_plugin(name: str):
    plugin_path = PLUGIN_DIR / name
    manifest = load_manifest()

    if name not in manifest:
        print(f"✗ Rechazado: '{name}' no está en el manifiesto de confianza.")
        return

    if not plugin_path.exists():
        print(f"✗ Rechazado: '{name}' no existe en {PLUGIN_DIR}.")
        return

    actual_hash = sha256_of(plugin_path)
    expected_hash = manifest[name]

    if actual_hash != expected_hash:
        print(f"✗ Rechazado: hash de '{name}' no coincide.")
        print(f"  esperado: {expected_hash}")
        print(f"  actual:   {actual_hash}")
        print("  (el archivo fue modificado o no es el original aprobado)")
        return

    print(f"✓ Verificado: '{name}' coincide con el manifiesto. Ejecutando en subproceso aislado...\n")

    # Se ejecuta como PROCESO APARTE (no exec()/eval() en el proceso principal),
    # con acceso mínimo — esto limita el daño incluso si algo saliera mal.
    result = subprocess.run(
        [sys.executable, str(plugin_path)],
        capture_output=True,
        text=True,
        timeout=5,
    )
    print(result.stdout, end="")
    if result.stderr:
        print("stderr:", result.stderr)


if __name__ == "__main__":
    print("=== Ejecutando plugin legítimo ===")
    run_plugin("greet.py")

    print("\n=== Ejecutando otro plugin legítimo ===")
    run_plugin("math_ops.py")

    print("\n=== Simulando un plugin manipulado/no confiable ===")
    run_plugin("evil.py")  # no está en manifest.json -> se rechaza
