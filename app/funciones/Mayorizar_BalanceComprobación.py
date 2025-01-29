from app.db_connection import obtener_conexion
import json
from datetime import datetime

def procesar_diario():
    """
    Recupera los asientos del diario desde la base de datos y los organiza por cuenta.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Consulta para obtener los registros del diario
    query = """
    SELECT fecha, cuenta, descripcion, debito, credito
    FROM diario
    """
    cursor.execute(query)
    asientos = cursor.fetchall()

    # Procesar los asientos
    cuentas = {}
    for asiento in asientos:
        cuenta = asiento[1]  # Asumimos que el índice 1 es "cuenta"
        if cuenta not in cuentas:
            cuentas[cuenta] = {"debito": 0, "credito": 0}
        cuentas[cuenta]["debito"] += asiento[3]  # Índice 3: débito
        cuentas[cuenta]["credito"] += asiento[4]  # Índice 4: crédito

    conexion.close()
    return cuentas

def mayorizar(cuentas):
    """
    Calcula los saldos finales para cada cuenta con base en los movimientos.
    """
    saldos = {}
    for cuenta, movimientos in cuentas.items():
        saldo = movimientos["debito"] - movimientos["credito"]
        saldos[cuenta] = saldo
    return saldos

def generar_balance_comprobacion(saldos):
    """
    Genera un balance de comprobación basado en los saldos calculados.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtener las descripciones de las cuentas desde la base de datos
    query = """
    SELECT numero_cuenta, descripcion
    FROM catalogo_cuentas
    """
    cursor.execute(query)
    catalogo = {row[0]: row[1] for row in cursor.fetchall()}  # Diccionario {cuenta: descripcion}

    # Preparar el balance de comprobación
    balance = []
    total_debe = 0
    total_haber = 0
    for cuenta, saldo in saldos.items():
        debe = saldo if saldo > 0 else 0
        haber = -saldo if saldo < 0 else 0
        total_debe += debe
        total_haber += haber
        balance.append({
            "cuenta": cuenta,
            "descripcion": catalogo.get(cuenta, "Sin descripción"),
            "debe": round(debe, 2),
            "haber": round(haber, 2)
        })

    conexion.close()
    return balance, total_debe, total_haber

def convertir_fecha(fecha):
    """
    Convierte una fecha en formato YYYY-MM-DD a DD-MM-YYYY.
    """
    return datetime.strptime(fecha, "%Y-%m-%d").strftime("%d-%m-%Y")

def main():
    """
    Ejecuta el proceso completo de mayorizar y generar el balance de comprobación.
    """
    print("Procesando diario...")
    cuentas = procesar_diario()

    print("Calculando saldos del mayor...")
    saldos = mayorizar(cuentas)

    print("Generando balance de comprobación...")
    balance, total_debe, total_haber = generar_balance_comprobacion(saldos)

    # Preparar salida en JSON
    salida = {
        "balance_de_comprobacion": balance,
        "total_debe": round(total_debe, 2),
        "total_haber": round(total_haber, 2),
        "fecha_generacion": convertir_fecha(datetime.now().strftime("%Y-%m-%d"))  # Fecha actual en formato dd-mm-yyyy
    }

    # Mostrar resultado en formato JSON
    print(json.dumps(salida, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
