"""Tarea: reporta espacio en disco usado en el volumen actual"""
import shutil


def run():
    total, used, free = shutil.disk_usage(".")
    pct_used = used / total * 100
    print(f"Disco: {used // (2**30)} GB usados de {total // (2**30)} GB ({pct_used:.1f}%)")
    if pct_used > 90:
        print("⚠ Advertencia: disco por encima del 90% de uso.")


if __name__ == "__main__":
    run()
