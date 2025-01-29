import sys
import os
import json

# Agregar la ruta del proyecto al PYTHONPATH para acceder a `Mayorizar_BalanceComprobación.py`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.funciones.Mayorizar_BalanceComprobación import mayorizar, formatear_mayor

def main():
    """
    Prueba las funciones de mayorizar y formatear los resultados.
    """
    try:
        # Solicitar fechas al usuario
        fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
        fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()

        if not fecha_inicio or not fecha_fin:
            print("⚠️ ERROR: Ambas fechas son obligatorias.")
            return

        # Llamar a la función mayorizar
        mayor = mayorizar(fecha_inicio, fecha_fin)

        # Formatear los resultados a JSON
        resultado_json = formatear_mayor(mayor)

        # Mostrar el JSON resultante
        if resultado_json:
            print("\n📌 Resultados del mayor:")
            print(resultado_json)
        else:
            print("❌ No se encontraron datos para el rango de fechas.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()
