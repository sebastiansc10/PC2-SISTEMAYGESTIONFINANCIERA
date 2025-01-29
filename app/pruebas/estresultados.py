import sys
import os
import json
from datetime import datetime

# Agregar la ruta raíz del proyecto al PYTHONPATH dinámicamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.funciones.EstadoResultados import calcular_estado_resultados

# 🔹 Manejo de Fechas: Verificar si se pasaron como argumentos
if len(sys.argv) == 3:
    fechainicio = sys.argv[1]
    fechafin = sys.argv[2]
else:
    # 🔹 Usar fechas por defecto (corregido a formato YYYY-MM-DD)
    fechainicio = '2009-04-01'
    fechafin = '2009-09-30'

# 🔹 Formatear fechas a YYYY-MM-DD si vienen en otro formato
try:
    fechainicio = datetime.strptime(fechainicio, "%Y-%m-%d").strftime("%Y-%m-%d")
    fechafin = datetime.strptime(fechafin, "%Y-%m-%d").strftime("%Y-%m-%d")
except ValueError:
    print("⚠️ ERROR: Formato de fecha incorrecto. Use YYYY-MM-DD.")
    sys.exit(1)

# 🔹 Ejecutar la función y mostrar el resultado
json_salida = calcular_estado_resultados(fechainicio, fechafin)
print(json_salida)
