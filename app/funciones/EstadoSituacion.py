from app.db_connection import obtener_conexion

import json

import json
from decimal import Decimal


def mayorizar():
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    t.ID_Cuenta,  -- Especificamos que `ID_Cuenta` proviene de la tabla `Transaccion`
                    c.Nombre_Cuenta,  -- Especificamos que `Nombre_Cuenta` proviene de la tabla `Cuenta`
                    SUM(CASE 
                            WHEN t.DH = 'Debe' THEN t.Cantidad  -- Especificamos que `DH` y `Cantidad` provienen de `Transaccion`
                            WHEN t.DH = 'Haber' THEN -t.Cantidad
                            ELSE 0 
                        END) AS Saldo
                FROM 
                    Transaccion t
                INNER JOIN 
                    Cuenta c ON c.ID_Cuenta = t.ID_Cuenta  -- Especificamos que la relación es entre las columnas `ID_Cuenta`
                GROUP BY 
                    t.ID_Cuenta, c.Nombre_Cuenta;  -- Aseguramos que también se agrupe por `Nombre_Cuenta`

                """
            )
            resultados=cursor.fetchall()
    return resultados       




def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Type not serializable")


def calcularbalance(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    c.id_cuenta, 
                    c.nombre_cuenta,
                    -- Columna 'Debe', si el saldo es mayor o igual que 0
                    CASE 
                        WHEN SUM(CASE 
                                    WHEN t.DH = 'Debe' THEN t.Cantidad
                                    WHEN t.DH = 'Haber' THEN -t.Cantidad
                                    ELSE 0 
                                END) >= 0 THEN SUM(CASE 
                                                    WHEN t.DH = 'Debe' THEN t.Cantidad
                                                    WHEN t.DH = 'Haber' THEN 0
                                                    ELSE 0 
                                                END)
                        ELSE 0
                    END AS Debe,
                    -- Columna 'Haber', si el saldo es menor que 0
                    CASE 
                        WHEN SUM(CASE 
                                    WHEN t.DH = 'Debe' THEN t.Cantidad
                                    WHEN t.DH = 'Haber' THEN -t.Cantidad
                                    ELSE 0 
                                END) < 0 THEN -1 * SUM(CASE 
                                                    WHEN t.DH = 'Haber' THEN -t.Cantidad
                                                    WHEN t.DH = 'Debe' THEN 0
                                                    ELSE 0 
                                                END)
                        ELSE 0
                    END AS Haber
                FROM 
                    transaccion t
                INNER JOIN 
                    diario d ON d.id_diario = t.id_diario
                INNER JOIN 
                    cuenta c ON c.id_cuenta = t.id_cuenta
                WHERE 
                    (%s <= d.fecha AND d.fecha <= %s)
                GROUP BY 
                    c.id_cuenta, c.nombre_cuenta
                """,
                (fechainicio, fechafin)  # Pasamos los parámetros para las fechas
            )
            # Obtén los resultados como lista de tuplas
            resultados = cursor.fetchall()

            # Obtén los nombres de las columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convierte los resultados a una lista de diccionarios
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]

    # Convierte la lista de diccionarios a JSON
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)


def situacion_activocorriente(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    c.id_cuenta, 
                    c.nombre_cuenta,
                    SUM(CASE 
                            WHEN t.DH = 'Debe' THEN t.Cantidad
                            WHEN t.DH = 'Haber' THEN -t.Cantidad
                            ELSE 0 
                        END) AS Saldo 
                FROM 
                    transaccion t
                INNER JOIN 
                    diario d ON d.id_diario = t.id_diario 
                INNER JOIN 
                    cuenta c ON c.id_cuenta = t.id_cuenta
                WHERE 
                    (c.id_elemento = 1 OR c.id_elemento = 2) 
                    AND (%s <= d.fecha AND d.fecha <= %s)
                GROUP BY 
                    t.ID_Cuenta, c.nombre_cuenta, c.id_cuenta;
                """,
                (fechainicio, fechafin)  # Pasamos los parámetros para las fechas
            )
            # Obtén los resultados como lista de tuplas
            resultados = cursor.fetchall()

            # Obtén los nombres de las columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convierte los resultados a una lista de diccionarios
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]

    # Convierte la lista de diccionarios a JSON
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)


def situacion_activonocorriente(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select c.id_cuenta , c.nombre_cuenta,
                -1 * SUM(CASE 
                            WHEN t.DH = 'Debe' THEN t.Cantidad  -- Especificamos que `DH` y `Cantidad` provienen de `Transaccion`
                            WHEN t.DH = 'Haber' THEN -t.Cantidad
                            ELSE 0 
                        END) AS Saldo 
                from transaccion t
                inner join diario d on d.id_diario = t.id_diario 
                inner join cuenta c on c.id_cuenta = t.id_cuenta
                where (c.id_elemento = 3) and (%s <= d.fecha and d.fecha <= %s)
                group by t.ID_Cuenta, c.nombre_cuenta, c.id_cuenta
                """,
                (fechainicio, fechafin)  # Pasamos los parámetros para las fechas
            )
            # Obtén los resultados como lista de tuplas
            resultados = cursor.fetchall()

            # Obtén los nombres de las columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convierte los resultados a una lista de diccionarios
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]

    # Convierte la lista de diccionarios a JSON
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)



def situacion_pasivo(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select c.id_cuenta , c.nombre_cuenta,
                -1*SUM(CASE 
                            WHEN t.DH = 'Debe' THEN t.Cantidad  -- Especificamos que `DH` y `Cantidad` provienen de `Transaccion`
                            WHEN t.DH = 'Haber' THEN -t.Cantidad
                            ELSE 0 
                        END) AS Saldo 
                from transaccion t
                inner join diario d on d.id_diario = t.id_diario 
                inner join cuenta c on c.id_cuenta = t.id_cuenta
                where (c.id_elemento = 4) and (%s <=d.fecha and d.fecha <= %s)
                group by t.ID_Cuenta, c.nombre_cuenta, c.id_cuenta
                """,
                (fechainicio, fechafin)  # Pasamos los parámetros para las fechas
            )
            # Obtén los resultados como lista de tuplas
            resultados = cursor.fetchall()

            # Obtén los nombres de las columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convierte los resultados a una lista de diccionarios
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]

    # Convierte la lista de diccionarios a JSON
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)

def situacion_pasivo(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select c.id_cuenta , c.nombre_cuenta,
                -1*SUM(CASE 
                            WHEN t.DH = 'Debe' THEN t.Cantidad  -- Especificamos que `DH` y `Cantidad` provienen de `Transaccion`
                            WHEN t.DH = 'Haber' THEN -t.Cantidad
                            ELSE 0 
                        END) AS Saldo 
                from transaccion t
                inner join diario d on d.id_diario = t.id_diario 
                inner join cuenta c on c.id_cuenta = t.id_cuenta
                where (c.id_elemento = 4) and (%s <=d.fecha and d.fecha <= %s)
                group by t.ID_Cuenta, c.nombre_cuenta, c.id_cuenta
                """,
                (fechainicio, fechafin)  # Pasamos los parámetros para las fechas
            )
            # Obtén los resultados como lista de tuplas
            resultados = cursor.fetchall()

            # Obtén los nombres de las columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convierte los resultados a una lista de diccionarios
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]

    # Convierte la lista de diccionarios a JSON
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)

def situacion_patrimonio(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select c.id_cuenta , c.nombre_cuenta,
                -1 * SUM(CASE 
                            WHEN t.DH = 'Debe' THEN t.Cantidad  -- Especificamos que `DH` y `Cantidad` provienen de `Transaccion`
                            WHEN t.DH = 'Haber' THEN -t.Cantidad
                            ELSE 0 
                        END) AS Saldo 
                from transaccion t
                inner join diario d on d.id_diario = t.id_diario 
                inner join cuenta c on c.id_cuenta = t.id_cuenta
                where (c.id_elemento = 5) and (%s <=d.fecha and d.fecha <= %s)
                group by t.ID_Cuenta, c.nombre_cuenta, c.id_cuenta
                """,
                (fechainicio, fechafin)  # Pasamos los parámetros para las fechas
            )
            # Obtén los resultados como lista de tuplas
            resultados = cursor.fetchall()

            # Obtén los nombres de las columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convierte los resultados a una lista de diccionarios
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]

    # Convierte la lista de diccionarios a JSON
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)



def situacion_totalactivocorriente(fechainicio, fechafin):
    resultados_json = situacion_activocorriente(fechainicio, fechafin)  # obtenemos los resultados como JSON
    
    # Convertimos el JSON de vuelta a un diccionario
    resultados = json.loads(resultados_json)  # Ahora `resultados` es una lista de diccionarios
    
    # Calculamos el total
    total_saldo = sum(fila['saldo'] for fila in resultados)
    
    # Si quieres devolver el resultado en formato JSON
    return json.dumps({"Total_Saldo": total_saldo}, indent=4, ensure_ascii=False, default=decimal_default)



def situacion_totalactivonocorriente(fechainicio, fechafin):
    resultados_json = situacion_activonocorriente(fechainicio, fechafin)  # obtenemos los resultados como JSON
    
    # Convertimos el JSON de vuelta a un diccionario
    resultados = json.loads(resultados_json)  # Ahora `resultados` es una lista de diccionarios
    
    # Calculamos el total
    total_saldo = sum(fila['saldo'] for fila in resultados)
    
    # Si quieres devolver el resultado en formato JSON
    return json.dumps({"Total_Saldo": total_saldo}, indent=4, ensure_ascii=False, default=decimal_default)


def situacion_totalpasivo(fechainicio, fechafin):
    resultados_json = situacion_pasivo(fechainicio, fechafin)  # obtenemos los resultados como JSON
    
    # Convertimos el JSON de vuelta a un diccionario
    resultados = json.loads(resultados_json)  # Ahora `resultados` es una lista de diccionarios
    
    # Calculamos el total
    total_saldo = sum(fila['saldo'] for fila in resultados)
    
    # Si quieres devolver el resultado en formato JSON
    return json.dumps({"Total_Saldo": total_saldo}, indent=4, ensure_ascii=False, default=decimal_default)


def situacion_totalpatrimonio(fechainicio, fechafin):
    resultados_json = situacion_patrimonio(fechainicio, fechafin)  # obtenemos los resultados como JSON
    
    # Convertimos el JSON de vuelta a un diccionario
    resultados = json.loads(resultados_json)  # Ahora `resultados` es una lista de diccionarios
    
    # Calculamos el total
    total_saldo = sum(fila['saldo'] for fila in resultados)
    
    # Si quieres devolver el resultado en formato JSON
    return json.dumps({"Total_Saldo": total_saldo}, indent=4, ensure_ascii=False, default=decimal_default)