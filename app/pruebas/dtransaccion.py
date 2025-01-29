from app.funciones.DiarioTransaccion import mostrar_transacciones_diario
import json

# Escoger el ID del diario a consultar
id_diario = 1

# Ejecutar la función y mostrar el resultado en JSON
resultado_json = mostrar_transacciones_diario(id_diario)
print(resultado_json)
