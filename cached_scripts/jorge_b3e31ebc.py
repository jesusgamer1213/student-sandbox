# Script de prueba - Estudiante: Jorge
# Ejercicio: Sumar números y listar contenido

def suma_numeros(numeros):
    """Suma una lista de números"""
    total = sum(numeros)
    return total

def procesar_datos():
    """Procesa datos educativos"""
    datos = [10, 20, 30, 40, 50]

    resultado = suma_numeros(datos)
    promedio = resultado / len(datos)

    print(f"📊 Datos procesados:")
    print(f"   - Números: {datos}")
    print(f"   - Suma total: {resultado}")
    print(f"   - Promedio: {promedio}")

    # Operaciones básicas permitidas
    multiplicado = resultado * 2
    print(f"   - Resultado × 2: {multiplicado}")

    return {
        "suma": resultado,
        "promedio": promedio,
        "cantidad": len(datos)
    }

if __name__ == "__main__":
    print("🎓 Script Educativo - Ejecución Legítima")
    print("-" * 40)
    resultado = procesar_datos()
    print("-" * 40)
    print("✅ Script ejecutado sin errores")
