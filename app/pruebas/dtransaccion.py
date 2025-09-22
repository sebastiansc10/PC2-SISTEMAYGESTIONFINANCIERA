import sys
import os
import json

# Agregar la ruta del proyecto al PYTHONPATH para acceder a `DiarioTransaccion.py`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.funciones.DiarioTransaccion import mostrar_transacciones

def main():
    """
    Prueba la función `mostrar_transacciones` solicitando la glosa y la fecha del diario.
    """
    try:
        glosa = input("Ingrese la glosa del diario: ").strip()
        fecha = input("Ingrese la fecha del diario (YYYY-MM-DD): ").strip()

        if not glosa or not fecha:
            print("⚠️ ERROR: La glosa y la fecha son obligatorias.")
            return
        
        resultado_json = mostrar_transacciones(glosa, fecha)  # Llamar a la función
        
        # Imprimir el JSON formateado
        print("\n📌 Transacciones encontradas para el Diario:")
        print(resultado_json)  # Se muestra el JSON directamente

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()
