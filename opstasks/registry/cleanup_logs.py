"""Tarea: elimina archivos .log de más de 7 días en ./logs"""
import time
from pathlib import Path

LOG_DIR = Path("logs")
MAX_AGE_DAYS = 7


def run():
    if not LOG_DIR.exists():
        print(f"No existe {LOG_DIR}, nada que limpiar.")
        return

    now = time.time()
    removed = 0
    for f in LOG_DIR.glob("*.log"):
        age_days = (now - f.stat().st_mtime) / 86400
        if age_days > MAX_AGE_DAYS:
            f.unlink()
            removed += 1

    print(f"Limpieza completa: {removed} archivo(s) .log eliminado(s).")


if __name__ == "__main__":
    run()
