import sys
import os
import json
from datetime import date

# Agregar la ruta raíz del proyecto al PYTHONPATH dinámicamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.funciones.EstadoResultados import calcular_estado_resultados

# Definir las fechas de prueba
fechainicio = "2025-01-01"
fechafin = str(date.today())  # Fecha actual

# Ejecutar la función y mostrar el resultado
json_salida = calcular_estado_resultados(fechainicio, fechafin)
print(json_salida)
