import sys, os
import json
from datetime import date

# Agregar la ruta raíz del proyecto al PYTHONPATH dinámicamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.funciones.EstadoResultados import calcular_estado_resultados

# Verificar si se pasaron fechas como argumentos
if len(sys.argv) == 3:
    fechainicio = sys.argv[1]
    fechafin = sys.argv[2]
else:
    # Si no se pasan fechas, usar valores por defecto
    fechainicio = "2025-01-01"
    fechafin = str(date.today())

# Ejecutar la función y mostrar el resultado
json_salida = calcular_estado_resultados(fechainicio, fechafin)
print(json_salida)
