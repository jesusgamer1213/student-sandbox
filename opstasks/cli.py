#!/usr/bin/env python3
"""
opstasks: CLI interno para correr tareas de mantenimiento estandarizadas
(limpieza de logs, chequeos de disco, etc.) sin que cada ingeniero copie
y pegue scripts a mano.

Las tareas viven en un registry central (repo/servidor del equipo de
plataforma). Este CLI las descarga bajo demanda, pero SOLO las ejecuta
si el hash SHA-256 coincide con opstasks.lock.json, que vive en el repo
del propio usuario/equipo y se revisa por PR como cualquier dependencia.

Esto es el mismo patrón que "pip install --require-hashes" o un
package-lock.json: la fuente de verdad de qué es confiable no es el
servidor remoto, es el lockfile que tú controlas.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOCKFILE = BASE_DIR / "opstasks.lock.json"
CACHE_DIR = BASE_DIR / ".cache"


def load_lockfile() -> dict:
    return json.loads(LOCKFILE.read_text())


def fetch_task_source(task_name: str, registry_url: str) -> bytes:
    """Descarga el código de la tarea desde el registry interno.

    En producción esto pega contra el servidor real del equipo por HTTPS.
    Para pruebas locales sin acceso a ese servidor, si existe una carpeta
    ./registry con el mismo archivo, se usa como stand-in del registry.
    """
    local_registry = BASE_DIR / "registry" / task_name
    if local_registry.exists():
        return local_registry.read_bytes()

    import requests  # import perezoso: solo se necesita si de verdad hay red

    resp = requests.get(f"{registry_url}/{task_name}", timeout=10)
    resp.raise_for_status()
    return resp.content


def verify_and_cache(task_name: str, source: bytes, expected_hash: str) -> Path:
    actual_hash = hashlib.sha256(source).hexdigest()
    if actual_hash != expected_hash:
        raise ValueError(
            f"Hash de '{task_name}' no coincide con opstasks.lock.json.\n"
            f"  esperado: {expected_hash}\n"
            f"  actual:   {actual_hash}\n"
            "Esto significa que el código en el registry cambió sin pasar "
            "por revisión, o que algo intermedio lo alteró. No se ejecuta."
        )

    CACHE_DIR.mkdir(exist_ok=True)
    cached_path = CACHE_DIR / task_name
    cached_path.write_bytes(source)
    return cached_path


def run_task(task_name: str):
    lock = load_lockfile()
    tasks = lock["tasks"]

    if task_name not in tasks:
        print(f"✗ '{task_name}' no está en opstasks.lock.json — no se puede ejecutar.")
        print("  Pide al equipo de plataforma que la agregue tras revisión.")
        sys.exit(1)

    entry = tasks[task_name]
    source = fetch_task_source(task_name, lock["registry_url"])

    try:
        cached_path = verify_and_cache(task_name, source, entry["sha256"])
    except ValueError as e:
        print(f"✗ {e}")
        sys.exit(1)

    print(f"✓ '{task_name}' v{entry['version']} verificada (revisada por {entry['reviewed_by']})")
    print(f"  Ejecutando en subproceso...\n")

    result = subprocess.run([sys.executable, str(cached_path)], text=True)
    sys.exit(result.returncode)


def list_tasks():
    lock = load_lockfile()
    print("Tareas disponibles:")
    for name, meta in lock["tasks"].items():
        print(f"  - {name} (v{meta['version']}, revisada por {meta['reviewed_by']})")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("run", "list"):
        print("Uso:")
        print("  opstasks list")
        print("  opstasks run <tarea>")
        sys.exit(1)

    if sys.argv[1] == "list":
        list_tasks()
    else:
        if len(sys.argv) < 3:
            print("Uso: opstasks run <tarea>")
            sys.exit(1)
        run_task(sys.argv[2])
