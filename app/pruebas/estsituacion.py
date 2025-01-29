from app.funciones.EstadoSituacion import situacion_activocorriente, situacion_activonocorriente, situacion_pasivo, situacion_patrimonio
from app.funciones.EstadoSituacion import situacion_totalactivocorriente, situacion_totalactivonocorriente, situacion_totalpasivo, situacion_totalpatrimonio
from app.funciones.EstadoSituacion import calcularbalance, total_debe, total_haber
from app.funciones.DiarioTransaccion import diariotransaccion

import json  # Importamos json para manejar la salida


fechainicio = '2009-04-01'
fechafin = '2009-09-30'

# Obtener resultados en formato JSON
resultados0_json = calcularbalance(fechainicio, fechafin)
resultados1_json = situacion_activocorriente(fechainicio, fechafin)
resultados2_json = situacion_activonocorriente(fechainicio, fechafin)
resultados3_json = situacion_pasivo(fechainicio, fechafin)
resultados4_json = situacion_patrimonio(fechainicio, fechafin)
#---
resultados11_json = situacion_totalactivocorriente(fechainicio, fechafin)
resultados12_json = situacion_totalactivonocorriente(fechainicio, fechafin)
resultados13_json = situacion_totalpasivo(fechainicio, fechafin)
resultados14_json = situacion_totalpatrimonio(fechainicio, fechafin)

total_debe_resultado = total_debe(fechainicio, fechafin)
total_haber_resultado = total_haber(fechainicio, fechafin)
totaldiario = diariotransaccion(fechainicio, fechafin)

# Imprimir el JSON formateado (opcional)

print("Diario y transacción:")
print(totaldiario)
print("--------------------------------")
"""
print("Balance de comprobación:")
print(resultados0_json)
print("--------------------------------")
print(f"Total 'Debe' desde: {total_debe_resultado}")
print(f"Total 'Haber' desde: {total_haber_resultado}")
print("--------------------------------")
print("Resultados en formato JSON de los activos corrientes:")
print(resultados1_json)
print("Total:")
print(resultados11_json)
print("--------------------------------")
print("Resultados en formato JSON de los activos no corrientes:")
print(resultados2_json)
print("Total:")
print(resultados12_json)
print("--------------------------------")
print("Resultados en formato JSON de los pasivos:")
print(resultados3_json)
print("Total:")
print(resultados13_json)
print("--------------------------------")
print("Resultados en formato JSON del patrimonio:")
print(resultados4_json)
print("Total:")
print(resultados14_json)
"""