import json
import sys
import os

# Agregar la ruta raíz del proyecto al PYTHONPATH dinámicamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.funciones.EstadoResultados import calcular_estado_resultados

# Simulación del JSON obtenido de Balance de Comprobación
import json

import json

balance_json = json.dumps([
    {"id_cuenta": 10, "nombre_cuenta": "Efectivo", "id_elemento": 1, "Debe": 10900, "Haber": 0},
    {"id_cuenta": 12, "nombre_cuenta": "Cuentas por cobrar", "id_elemento": 1, "Debe": 0, "Haber": 0},
    {"id_cuenta": 20, "nombre_cuenta": "Mercadería", "id_elemento": 2, "Debe": 2500, "Haber": 0},
    {"id_cuenta": 33, "nombre_cuenta": "Activo fijo", "id_elemento": 3, "Debe": 3000, "Haber": 0},
    {"id_cuenta": 39, "nombre_cuenta": "Depreciación acumulada", "id_elemento": 3, "Debe": 0, "Haber": 135},
    {"id_cuenta": 41, "nombre_cuenta": "Remuneraciones por pagar", "id_elemento": 4, "Debe": 0, "Haber": 1200},
    {"id_cuenta": 42, "nombre_cuenta": "Cuentas por pagar comerciales", "id_elemento": 4, "Debe": 0, "Haber": 2000},
    {"id_cuenta": 50, "nombre_cuenta": "Capital social", "id_elemento": 5, "Debe": 0, "Haber": 10000},
    
    # 🔹 Gastos operativos (ID_Elemento = 6)
    {"id_cuenta": 62, "nombre_cuenta": "Gastos de personal", "id_elemento": 6, "Debe": 1200, "Haber": 0},
    {"id_cuenta": 63, "nombre_cuenta": "Gastos de alquiler", "id_elemento": 6, "Debe": 1300, "Haber": 0},
    {"id_cuenta": 66, "nombre_cuenta": "Pérdidas de activo", "id_elemento": 6, "Debe": 600, "Haber": 0},
    {"id_cuenta": 68, "nombre_cuenta": "Gastos de depreciación", "id_elemento": 6, "Debe": 135, "Haber": 0},
    {"id_cuenta": 69, "nombre_cuenta": "Costo de venta", "id_elemento": 6, "Debe": 3400, "Haber": 0},

    # 🔹 Ingresos (ID_Elemento = 7)
    {"id_cuenta": 70, "nombre_cuenta": "Ventas", "id_elemento": 7, "Debe": 0, "Haber": 8700},
    {"id_cuenta": 75, "nombre_cuenta": "Otros ingresos de gestión", "id_elemento": 7, "Debe": 0, "Haber": 1000}
])


# Ejecutar la función y mostrar el resultado
json_salida = calcular_estado_resultados(balance_json)
print(json_salida)
