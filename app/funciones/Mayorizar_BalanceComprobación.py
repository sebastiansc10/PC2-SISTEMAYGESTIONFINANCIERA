from app.db_connection import obtener_conexion
import json
from decimal import Decimal


def mayorizar(fecha_inicio, fecha_fin):
    """
    Obtiene los movimientos contables agrupados por cuenta y fecha, y calcula el saldo absoluto.
    :param fecha_inicio: Fecha inicial del rango (YYYY-MM-DD).
    :param fecha_fin: Fecha final del rango (YYYY-MM-DD).
    :return: Lista de diccionarios con los resultados del mayor.
    """
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                # Consulta SQL para obtener movimientos agrupados
                cursor.execute(
                    """
                    SELECT 
                        c.id_cuenta,
                        c.nombre_cuenta,
                        d.fecha,
                        SUM(CASE WHEN t.dh = 'Debe' THEN t.cantidad ELSE 0 END) AS debe,
                        SUM(CASE WHEN t.dh = 'Haber' THEN t.cantidad ELSE 0 END) AS haber
                    FROM transaccion t
                    INNER JOIN cuenta c ON t.id_cuenta = c.id_cuenta
                    INNER JOIN diario d ON t.id_diario = d.id_diario
                    WHERE d.fecha BETWEEN %s AND %s
                    GROUP BY c.id_cuenta, c.nombre_cuenta, d.fecha
                    ORDER BY c.id_cuenta, d.fecha;
                    """,
                    (fecha_inicio, fecha_fin)
                )

                resultados = cursor.fetchall()

                # Procesar resultados
                mayor = [
                    {
                        "id_cuenta": resultado[0],
                        "nombre_cuenta": resultado[1],
                        "fecha": resultado[2].strftime("%Y-%m-%d"),  # Convertir fecha a string
                        "debe": float(resultado[3]) if resultado[3] else 0.0,
                        "haber": float(resultado[4]) if resultado[4] else 0.0,
                        "saldo": abs(float(resultado[3] - resultado[4]))  # Valor absoluto del saldo
                    }
                    for resultado in resultados
                ]

                return mayor
    except Exception as e:
        print(f"❌ Error al calcular el mayor: {e}")
        return None


def formatear_mayor(mayor):
    """
    Convierte los datos del mayor a formato JSON.
    :param mayor: Lista de diccionarios con los datos del mayor.
    :return: JSON formateado como string.
    """
    try:
        if not mayor:
            return json.dumps({"error": "No se encontraron datos para el rango especificado."}, indent=4)

        return json.dumps(mayor, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error al formatear los datos: {e}")
        return None
