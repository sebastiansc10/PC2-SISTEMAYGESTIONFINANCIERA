import json
from app.funciones.EstadoSituacion import calcularbalance

# 🔹 Definimos las cuentas específicas según ID_Cuenta en la base de datos
CATEGORIAS_CUENTAS = {
    "ventas": [70],  # Ingresos por ventas
    "costo_ventas": [69],  # Costos de ventas
    "gastos_operativos": [62, 63, 68],  # Gastos operativos específicos
    "otros_ingresos": [75],  # Otros ingresos no operativos
    "perdidas": [66],  # Pérdidas extraordinarias
    "impuesto_renta": [88]  # Impuestos a la renta
}

def calcular_estado_resultados(fechainicio, fechafin):
    """
    Obtiene el Balance de Comprobación desde `calcularbalance` y genera el Estado de Resultados.
    """

    # 🔹 Obtener datos del balance de comprobación como JSON
    balance_json = calcularbalance(fechainicio, fechafin)

    # 🔹 Verificar qué devuelve calcularbalance()
    print("📌 JSON devuelto por calcularbalance:\n", balance_json)  # <<<< Agregado para depuración

    # 🔹 Convertir JSON a lista de diccionarios
    balance = json.loads(balance_json)

    # 🔹 Si el balance está vacío, detener la ejecución
    if not balance:
        print("⚠️ ERROR: No se encontraron datos en el balance de comprobación.")
        return json.dumps({"error": "No hay datos en el balance"}, indent=4)

    # 🔹 Función para obtener totales de cuentas específicas
    def obtener_total_por_cuentas(lista_cuentas, tipo):
        """
        Obtiene el total de Debe o Haber según una lista de cuentas específicas.
        :param lista_cuentas: Lista de ID_Cuenta a considerar.
        :param tipo: 'Debe' o 'Haber'.
        :return: Suma total del tipo seleccionado.
        """
        return sum(item.get(tipo.lower(), 0) for item in balance if item["id_cuenta"] in lista_cuentas)

    # 🔹 Obtener desglose de gastos operativos
    def obtener_gastos_operativos():
        """
        Obtiene un desglose automático de los gastos operativos sin incluir costos de venta ni pérdidas.
        :return: Diccionario con los detalles de los gastos operativos.
        """
        gastos = {}
        total_gastos = 0

        for item in balance:
            if item["id_cuenta"] in CATEGORIAS_CUENTAS["gastos_operativos"] and item.get("debe", 0) > 0:
                cuenta = item["nombre_cuenta"]
                monto = item.get("debe", 0)
                gastos[cuenta] = monto
                total_gastos += monto

        return {"detalle": gastos, "total_gastos_operativos": total_gastos}

    # 🔹 Obtener valores corregidos desde el Balance de Comprobación
    ventas = obtener_total_por_cuentas(CATEGORIAS_CUENTAS["ventas"], "Haber")
    costo_ventas = obtener_total_por_cuentas(CATEGORIAS_CUENTAS["costo_ventas"], "Debe")
    otros_ingresos = obtener_total_por_cuentas(CATEGORIAS_CUENTAS["otros_ingresos"], "Haber")
    perdidas = obtener_total_por_cuentas(CATEGORIAS_CUENTAS["perdidas"], "Debe")
    impuesto_renta = obtener_total_por_cuentas(CATEGORIAS_CUENTAS["impuesto_renta"], "Debe")

    # 🔹 Obtener desglose de gastos operativos
    gastos_operativos = obtener_gastos_operativos()
    total_gastos_operativos = gastos_operativos["total_gastos_operativos"]

    # 🔹 Cálculos del Estado de Resultados
    utilidad_bruta = ventas - costo_ventas
    utilidad_operativa = utilidad_bruta - total_gastos_operativos
    utilidad_antes_impuestos = utilidad_operativa + otros_ingresos - perdidas
    utilidad_neta = utilidad_antes_impuestos - impuesto_renta

    # 🔹 Construcción del JSON de salida
    resultado = {
        "ventas": ventas,
        "costo_ventas": costo_ventas,
        "utilidad_bruta": utilidad_bruta,
        "gastos_operativos": gastos_operativos,
        "utilidad_operativa": utilidad_operativa,
        "otros_ingresos": otros_ingresos,
        "perdidas": perdidas,
        "utilidad_antes_impuestos": utilidad_antes_impuestos,
        "impuesto_renta": impuesto_renta,
        "utilidad_neta": utilidad_neta
    }

    return json.dumps(resultado, indent=4, ensure_ascii=False)
