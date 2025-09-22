import json
from app.funciones.EstadoSituacion import calcularbalance
from app.db_connection import obtener_conexion
import decimal

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)  # Convierte Decimal a float
    raise TypeError("Type not serializable")

def calcularresultado(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT c.nombre_cuenta,
                ABS(SUM(CASE 
                        WHEN t.DH = 'Debe' THEN t.Cantidad  
                        WHEN t.DH = 'Haber' THEN -t.Cantidad
                        ELSE 0 
                    END)) AS saldo
                FROM cuenta c 
                INNER JOIN transaccion t ON c.id_cuenta = t.id_cuenta
                INNER JOIN diario d ON d.id_diario = t.id_diario 
                WHERE c.id_cuenta IN (62, 63, 64, 66, 67, 68, 69, 70, 75, 77, 88) 
                AND (%s <= d.fecha AND d.fecha <= %s)
                GROUP BY c.nombre_cuenta;
                """,
                (fechainicio, fechafin)
            )
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]
    
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)

# 🔹 Definimos el mapeo de cuentas
mapeo_cuentas = {
    "Costo de ventas": "costo_ventas",
    "Gastos de personal, directores y gerentes": "gasto_personal",
    "Gastos de servicios prestados por terceros": "gasto_servicios",
    "Otros ingresos de gestión": "otros_ingresos",
    "Valuación y deterioro de activos y provisiones": "gasto_devaluacion",
    "Ventas": "ventas_netas",
    "Pérdida por medición de activos no financieros al valor razonable": "perdidas",
    "Impuesto a la renta": "impuesto_renta"
}

def calcular_estado_resultados(fechainicio, fechafin):
    """
    Obtiene el Balance de Comprobación desde `calcularbalance` y genera el Estado de Resultados.
    """
    json_resultado = calcularresultado(fechainicio, fechafin)
    datos = json.loads(json_resultado)

    # Inicializamos las variables en un diccionario
    valores_cuentas = {key: 0.0 for key in mapeo_cuentas.values()}
    
    # Asignar valores según el JSON
    for cuenta in datos:
        nombre_cuenta = cuenta["nombre_cuenta"]
        saldo = cuenta["saldo"]
        if nombre_cuenta in mapeo_cuentas:
            valores_cuentas[mapeo_cuentas[nombre_cuenta]] = saldo
    
    # Extraer los valores actualizados
    costo_ventas = valores_cuentas["costo_ventas"]
    gasto_personal = valores_cuentas["gasto_personal"]
    gasto_servicios = valores_cuentas["gasto_servicios"]
    otros_ingresos = valores_cuentas["otros_ingresos"]
    gasto_devaluacion = valores_cuentas["gasto_devaluacion"]
    ventas_netas = valores_cuentas["ventas_netas"]
    perdidas = valores_cuentas["perdidas"]
    impuesto_renta = valores_cuentas["impuesto_renta"]
    
    # 🔹 Cálculos del Estado de Resultados
    gastos_operativos = gasto_personal + gasto_servicios + gasto_devaluacion
    utilidad_bruta = ventas_netas - costo_ventas
    utilidad_operativa = utilidad_bruta - gastos_operativos
    utilidad_antes_impuestos = utilidad_operativa + otros_ingresos - perdidas
    utilidad_neta = utilidad_antes_impuestos - impuesto_renta
    
    # 🔹 Construcción del JSON de salida
    resultado = {
        "ventas": ventas_netas,
        "costo_ventas": costo_ventas,
        "utilidad_bruta": utilidad_bruta,
        "Gastos de personal": gasto_personal,
        "Gastos de servicios": gasto_servicios,
        "Devaluación": gasto_devaluacion,
        "gastos_operativos": gastos_operativos,
        "utilidad_operativa": utilidad_operativa,
        "otros_ingresos": otros_ingresos,
        "perdidas": perdidas,
        "utilidad_antes_impuestos": utilidad_antes_impuestos,
        "impuesto_renta": impuesto_renta,
        "utilidad_neta": utilidad_neta
    }
    
    return json.dumps(resultado, indent=4, ensure_ascii=False)



def calcularutilidad(fechainicio, fechafin):
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT c.nombre_cuenta,
                ABS(SUM(CASE 
                        WHEN t.DH = 'Debe' THEN t.Cantidad  
                        WHEN t.DH = 'Haber' THEN -t.Cantidad
                        ELSE 0 
                    END)) AS saldo
                FROM cuenta c 
                INNER JOIN transaccion t ON c.id_cuenta = t.id_cuenta
                INNER JOIN diario d ON d.id_diario = t.id_diario 
                WHERE c.id_cuenta IN (62, 63, 64, 66, 67, 68, 69, 70, 75, 77, 88) 
                AND (%s <= d.fecha AND d.fecha <= %s)
                GROUP BY c.nombre_cuenta;
                """,
                (fechainicio, fechafin)
            )
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]
    
    return json.dumps(resultados_dict, indent=4, ensure_ascii=False, default=decimal_default)

# 🔹 Definimos el mapeo de cuentas
mapeo_cuentas = {
    "Costo de ventas": "costo_ventas",
    "Gastos de personal, directores y gerentes": "gasto_personal",
    "Gastos de servicios prestados por terceros": "gasto_servicios",
    "Otros ingresos de gestión": "otros_ingresos",
    "Valuación y deterioro de activos y provisiones": "gasto_devaluacion",
    "Ventas": "ventas_netas",
    "Pérdida por medición de activos no financieros al valor razonable": "perdidas",
    "Impuesto a la renta": "impuesto_renta"
}

def utilidadantes(fechainicio, fechafin):
    """
    Obtiene el Balance de Comprobación desde `calcularbalance` y genera el Estado de Resultados.
    """
    json_resultado = calcularresultado(fechainicio, fechafin)
    datos = json.loads(json_resultado)

    # Inicializamos las variables en un diccionario
    valores_cuentas = {key: 0.0 for key in mapeo_cuentas.values()}
    
    # Asignar valores según el JSON
    for cuenta in datos:
        nombre_cuenta = cuenta["nombre_cuenta"]
        saldo = cuenta["saldo"]
        if nombre_cuenta in mapeo_cuentas:
            valores_cuentas[mapeo_cuentas[nombre_cuenta]] = saldo
    
    # Extraer los valores actualizados
    costo_ventas = valores_cuentas["costo_ventas"]
    gasto_personal = valores_cuentas["gasto_personal"]
    gasto_servicios = valores_cuentas["gasto_servicios"]
    otros_ingresos = valores_cuentas["otros_ingresos"]
    gasto_devaluacion = valores_cuentas["gasto_devaluacion"]
    ventas_netas = valores_cuentas["ventas_netas"]
    perdidas = valores_cuentas["perdidas"]
    impuesto_renta = valores_cuentas["impuesto_renta"]
    
    # 🔹 Cálculos del Estado de Resultados
    gastos_operativos = gasto_personal + gasto_servicios + gasto_devaluacion
    utilidad_bruta = ventas_netas - costo_ventas
    utilidad_operativa = utilidad_bruta - gastos_operativos
    utilidad_antes_impuestos = utilidad_operativa + otros_ingresos - perdidas
    utilidad_neta = utilidad_antes_impuestos - impuesto_renta
    
    # 🔹 Construcción del JSON de salida
    resultado = {
        "utilidad_antes_impuestos": utilidad_antes_impuestos,
    }
    
    return json.dumps(resultado, indent=4, ensure_ascii=False)