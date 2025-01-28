from app.db_connection import obtener_conexion

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

