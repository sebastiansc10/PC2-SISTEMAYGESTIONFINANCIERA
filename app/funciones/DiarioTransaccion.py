import decimal
from app.db_connection import obtener_conexion
import json
from decimal import Decimal
from datetime import date


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)  # Convierte Decimal a float
    raise TypeError("Type not serializable")

def mostrar_diario():
    """Devuelve un JSON con las cuentas disponibles en la tabla Diario como una lista de diccionarios."""
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT fecha, glosa FROM diario ORDER BY fecha ASC;")
            cuentas = cursor.fetchall()

            # Convertimos la lista de tuplas en una lista de diccionarios
            resultado = [{"fecha": cuenta[0].strftime('%Y-%m-%d'), "glosa": cuenta[1]} for cuenta in cuentas]

            return json.dumps(resultado, indent=4, ensure_ascii=False)  # Convierte la lista a JSON



def registrar_diario(fecha, glosa):
    """Registra un nuevo asiento en la tabla Diario y devuelve su ID."""
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Diario (Fecha, Glosa)
                    VALUES (%s, %s)
                    RETURNING ID_Diario;
                """, (fecha, glosa))
                id_diario = cursor.fetchone()[0]
                conn.commit()
                print(f"✅ Asiento registrado con ID {id_diario}")
                return id_diario
    except Exception as e:
        print(f"❌ Error al registrar el asiento: {e}")
        return None

def eliminar_diario(fecha, glosa):
    """Elimina un asiento en la tabla Diario y todas sus transacciones asociadas."""
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                # Verificar si existe el diario con la fecha y glosa proporcionadas
                cursor.execute("SELECT id_diario FROM Diario WHERE fecha = %s AND glosa = %s;", (fecha, glosa))
                resultado = cursor.fetchone()

                if not resultado:
                    print(f"⚠️ No se encontró un diario con fecha {fecha} y glosa '{glosa}'.")
                    return False

                id_diario = resultado[0]

                # Eliminar el diario, lo que también eliminará en cascada las transacciones asociadas
                cursor.execute("DELETE FROM Diario WHERE id_diario = %s;", (id_diario,))

                conn.commit()
                print(f"✅ Diario con ID {id_diario} eliminado correctamente.")
                return True
    except Exception as e:
        print(f"❌ Error al eliminar el diario: {e}")
        return False

def actualizar_diario(fecha, glosa, fechaantigua, glosaantigua):
    """Actualiza un asiento en la tabla Diario y devuelve su ID actualizado."""
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                # Actualizar el diario
                cursor.execute("""
                    UPDATE diario 
                    SET glosa = %s, fecha = %s 
                    WHERE glosa = %s AND fecha = %s
                    RETURNING id_diario;
                """, (glosa, fecha, glosaantigua, fechaantigua))

                id_diario = cursor.fetchone()  # Obtener el ID actualizado

                if id_diario:  # Si hay un resultado, se confirma la transacción
                    conn.commit()
                    print(f"✅ Asiento actualizado con ID {id_diario[0]}")
                    return id_diario[0]
                else:
                    print("⚠️ No se encontró ningún asiento con esos datos.")
                    return None
    except Exception as e:
        print(f"❌ Error al actualizar el asiento: {e}")
        return None

    

def obtener_cuentas():
    """Devuelve un diccionario con las cuentas disponibles en la tabla Cuenta."""
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID_Cuenta, Nombre_Cuenta FROM Cuenta ORDER BY ID_Cuenta;")
            cuentas = cursor.fetchall()
            return {cuenta[0]: cuenta[1] for cuenta in cuentas}

def registrar_asiento_completo():
    """Flujo interactivo para registrar un asiento contable completo."""
    fecha = input("Ingrese la fecha del asiento (YYYY-MM-DD): ")
    glosa = input("Ingrese la glosa (descripción): ")

    # Registrar el asiento de diario
    id_diario = registrar_diario(fecha, glosa)
    print(f"Asiento registrado con ID: {id_diario}")

    while True:
        # Obtener las cuentas disponibles
        cuentas_disponibles = obtener_cuentas()
        print("\nCuentas disponibles:")
        for id_cuenta, nombre_cuenta in cuentas_disponibles.items():
            print(f"{id_cuenta}: {nombre_cuenta}")

        # Solicitar la selección de cuenta
        id_cuenta = int(input("Seleccione una cuenta por su ID: "))
        if id_cuenta not in cuentas_disponibles:
            print("Cuenta no válida. Intente nuevamente.")
            continue

        # Seleccionar el tipo de movimiento
        while True:
            dh = input("Indique el tipo de movimiento (Debe/Haber): ").capitalize()
            if dh in ["Debe", "Haber"]:
                break
            else:
                print("Valor inválido. Debe ser 'Debe' o 'Haber'.")

        # Ingresar el monto
        while True:
            try:
                cantidad = float(input("Ingrese el monto: "))
                if cantidad > 0:
                    break
                else:
                    print("El monto debe ser mayor a 0.")
            except ValueError:
                print("Ingrese un número válido.")

        # Preguntar si desea agregar otra transacción
        continuar = input("¿Desea agregar otra transacción a este asiento? (s/n): ").lower()
        if continuar != 's':
            break

def decimal_default(obj):
    """Convierte objetos Decimal a float para JSON."""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def mostrar_transacciones(glosa, fecha):
    """
    Devuelve un JSON con las transacciones de un diario específico.
    :param glosa: Glosa del diario.
    :param fecha: Fecha del diario (YYYY-MM-DD).
    :return: JSON con las transacciones del diario.
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    t.cantidad, 
                    t.dh, 
                    c.nombre_cuenta,
                    c.id_cuenta 
                FROM transaccion t
                INNER JOIN cuenta c ON t.id_cuenta = c.id_cuenta
                WHERE t.id_diario = (SELECT d.id_diario FROM diario d WHERE d.glosa = %s AND d.fecha = %s)
                ORDER BY t.dh DESC, t.cantidad DESC;
                """, 
                (glosa, fecha)
            )
            transacciones = cursor.fetchall()

            # Formatear los resultados en un diccionario
            resultado = [
                {
                    "cantidad": float(transaccion[0]),  # Convertir Decimal a float
                    "tipo": transaccion[1],  # 'Debe' o 'Haber'
                    "cuenta": transaccion[2],  # Nombre de la cuenta
                    "id_cuenta": transaccion[3]
                }
                for transaccion in transacciones
            ]
            
            return json.dumps(resultado, indent=4, ensure_ascii=False, default=decimal_default)  # Convierte a JSON
        


def diariotransaccion(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    d.fecha,
                    d.glosa,
                    json_agg(
                        json_build_object(
                            'cantidad', t.cantidad,
                            'dh', t.dh,
                            'id_cuenta', c.id_cuenta,
                            'nombre_cuenta', c.nombre_cuenta
                        )
                    ) AS transacciones
                FROM diario d
                INNER JOIN transaccion t ON d.id_diario = t.id_diario
                INNER JOIN cuenta c ON c.id_cuenta = t.id_cuenta
                WHERE (%s <= d.fecha AND d.fecha <= %s)
                GROUP BY d.fecha, d.glosa
                ORDER BY d.fecha;
                """,
                (fechainicio, fechafin)  
            )
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]

            # Convertir valores no serializables
            def convertir_valores(obj):
                if isinstance(obj, decimal.Decimal):
                    return float(obj)
                elif isinstance(obj, date):  # Convierte date a string
                    return obj.isoformat()
                return obj

            # Aplicamos la conversión a cada diccionario
            for resultado in resultados_dict:
                for key, value in resultado.items():
                    if isinstance(value, list):  # Si 'transacciones' es una lista, iteramos
                        resultado[key] = [
                            {k: convertir_valores(v) for k, v in transaccion.items()}
                            for transaccion in value
                        ]
                    else:
                        resultado[key] = convertir_valores(value)

    return json.dumps(resultados_dict, indent=4, ensure_ascii=False)

def registrar_nueva_transaccion(id_cuenta, dh, cantidad, glosa, fecha):
    """
    Registra una nueva transacción para un diario existente.
    
    Args:
        id_cuenta: ID de la cuenta
        dh: 'Debe' o 'Haber'
        cantidad: Monto de la transacción
        glosa: Glosa del diario existente
        fecha: Fecha del diario existente
    
    Returns:
        bool: True si se registró correctamente, False en caso contrario
    """
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cursor:
                # Primero obtener el ID del diario
                cursor.execute(
                    "SELECT id_diario FROM diario WHERE glosa = %s AND fecha = %s",
                    (glosa, fecha)
                )
                resultado = cursor.fetchone()
                if not resultado:
                    print("❌ No se encontró el diario especificado")
                    return False
                
                id_diario = resultado[0]
                
                # Registrar la nueva transacción
                cursor.execute("""
                    INSERT INTO Transaccion (Cantidad, DH, ID_Diario, ID_Cuenta)
                    VALUES (%s, %s, %s, %s)
                    RETURNING ID_Transaccion;
                """, (cantidad, dh, id_diario, id_cuenta))
                
                id_transaccion = cursor.fetchone()[0]
                conn.commit()
                print(f"✅ Transacción registrada con ID {id_transaccion}")
                return True
    except Exception as e:
        print(f"❌ Error al registrar la transacción: {e}")
        return False
    


def eliminar_transaccion(glosa, fecha, id_cuenta, cantidad, dh):
    """
    Elimina una transacción de un diario específico.
    :param glosa: Glosa del diario.
    :param fecha: Fecha del diario (YYYY-MM-DD).
    :param id_cuenta: ID de la cuenta.
    :param cantidad: Monto de la transacción.
    :param dh: Tipo de movimiento ('D' para Débito, 'H' para Crédito).
    :return: JSON con el resultado de la operación.
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM transaccion 
                WHERE id_diario = (SELECT d.id_diario FROM diario d WHERE d.glosa = %s AND d.fecha = %s) 
                AND id_cuenta = %s 
                AND cantidad = %s 
                AND dh = %s;
                """, 
                (glosa, fecha, id_cuenta, cantidad, dh)
            )
            
            # Verificar si se eliminó alguna fila
            filas_afectadas = cursor.rowcount
            conn.commit()
            
            return json.dumps(
                {"mensaje": "Transacción eliminada correctamente." if filas_afectadas > 0 else "No se encontró la transacción."},
                indent=4,
                ensure_ascii=False
            )

import json

def actualizar_transaccion(glosa, fecha, id_cuenta, cantidad_actual, dh_actual, nueva_cantidad, nuevo_dh, nueva_cuenta):
    """
    Actualiza una transacción en la tabla 'transaccion'.
    
    :param glosa: Glosa del diario.
    :param fecha: Fecha del diario (YYYY-MM-DD).
    :param id_cuenta: ID de la cuenta a modificar.
    :param cantidad_actual: Cantidad actual en la transacción.
    :param dh_actual: Tipo actual de movimiento ('D' o 'H').
    :param nueva_cantidad: Nuevo valor de la cantidad.
    :param nuevo_dh: Nuevo tipo de movimiento ('D' o 'H').
    :param nueva_cuenta: Nuevo ID de la cuenta.
    :return: JSON con el resultado de la operación.
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE transaccion 
                SET cantidad = %s, dh = %s, id_cuenta = %s
                WHERE id_diario = (
                    SELECT id_diario FROM diario WHERE glosa = %s AND fecha = %s
                )
                AND id_cuenta = %s 
                AND cantidad = %s 
                AND dh = %s;
                """, 
                (nueva_cantidad, nuevo_dh, nueva_cuenta, glosa, fecha, id_cuenta, cantidad_actual, dh_actual)
            )
            
            filas_afectadas = cursor.rowcount
            conn.commit()
            
            return json.dumps(
                {"mensaje": "Transacción actualizada correctamente." if filas_afectadas > 0 else "No se encontró la transacción."},
                indent=4,
                ensure_ascii=False
            )

def truncar_diario():
    """Trunca la tabla Diario, eliminando todos los registros."""
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("truncate diario cascade;")
            conn.commit()  # Confirmar los cambios
    return json.dumps({"mensaje": "Tabla Diario truncada correctamente"})