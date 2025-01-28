from app.funciones.EstadoSituacion import situacion_activocorriente

fechainicio = '2025-01-01'
fechafin = '2025-01-27'
resultados = situacion_activocorriente(fechainicio, fechafin)

for fila in resultados:
    print(fila)
