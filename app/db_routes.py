# endpoints.py

from fastapi import APIRouter, HTTPException
from app.db_functions import mayorizar, nueva_transaccion

# Crear un router para los endpoints
router = APIRouter()

@router.get("/api/mayor")
async def mayorizar_end():
    # Llamar a la función que obtiene los datos
    resultados = mayorizar()

    # Convertir los resultados a un formato adecuado para JSON
    mayor = [{"Código cuenta": fila[0], "Nombre cuenta": fila[1], "Saldo": fila[2]} for fila in resultados]

    return mayor

@router.post("/api/insertar_transaccion")
async def insertar_transaccion_end(cantidad: float, dh: str, id_diario: int, id_cuenta: int):
    try:
        # Llamar a la función para insertar la transacción
        nueva_transaccion(cantidad, dh, id_diario, id_cuenta)
        return {"mensaje": "Transacción insertada correctamente"}
    except Exception as e:
        # Si ocurre un error, devolver un mensaje de error
        raise HTTPException(status_code=400, detail=f"Error al insertar transacción: {str(e)}")