import json
from app.funciones.EstadoSituacion import calcularbalance

# 🔹 Definimos las categorías de cuentas según ID_Cuenta en la base de datos
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
    
    # 🔹 Ver qué devuelve calcularbalance()
    # print("\n📌 JSON devuelto por calcularbalance:\n", balance_json)  

    # 🔹 Convertir JSON a lista de diccionarios
    balance = json.loads(balance_json)

    # 🔹 Si el balance está vacío, detener la ejecución
    if not balance:
        print("⚠️ ERROR: No se encontraron datos en el balance de comprobación.")
        return json.dumps({"error": "No hay datos en el balance"}, indent=4)

    # 🔹 Función generalizada para obtener saldo neto (sum(Haber) - sum(Debe)) y aplicar valor absoluto
    def obtener_saldo_neto(lista_cuentas, nombre):
        """
        Obtiene el saldo neto de una lista de cuentas, asegurando valores positivos.
        :param lista_cuentas: Lista de ID_Cuenta a considerar.
        :param nombre: Nombre de la categoría (para depuración).
        :return: Suma neta de los valores (SUM(Haber) - SUM(Debe)) con valor absoluto.
        """
        total_haber = sum(item.get("haber", 0) for item in balance if item["id_cuenta"] in lista_cuentas)
        total_debe = sum(item.get("debe", 0) for item in balance if item["id_cuenta"] in lista_cuentas)
        
        saldo = abs(total_haber - total_debe)  # 🔹 Asegura que el saldo neto sea positivo

        # print(f"✅ {nombre}: Haber ({total_haber}) - Debe ({total_debe}) = {saldo}")  # 🔹 Ver el cálculo en cada paso
        return saldo

    # 🔹 Obtener desglose de gastos operativos
    def obtener_gastos_operativos():
        """
        Obtiene un desglose automático de los gastos operativos sin incluir costos de venta ni pérdidas.
        :return: Diccionario con los detalles de los gastos operativos.
        """
        gastos = {}
        total_gastos = 0

        for item in balance:
            if item["id_cuenta"] in CATEGORIAS_CUENTAS["gastos_operativos"]:
                cuenta = item["nombre_cuenta"]
                monto = abs(item.get("debe", 0) - item.get("haber", 0))
                gastos[cuenta] = monto
                total_gastos += monto
                # print(f"📌 Gastos Operativos -> {cuenta}: {monto}")  # 🔹 Ver desglose de gastos

        return {"detalle": gastos, "total_gastos_operativos": total_gastos}

    # 🔹 Aplicar la función generalizada a cada categoría
    ventas_netas = obtener_saldo_neto(CATEGORIAS_CUENTAS["ventas"], "Ventas Netas")
    costo_ventas = obtener_saldo_neto(CATEGORIAS_CUENTAS["costo_ventas"], "Costo de Ventas")
    otros_ingresos = obtener_saldo_neto(CATEGORIAS_CUENTAS["otros_ingresos"], "Otros Ingresos")
    perdidas = obtener_saldo_neto(CATEGORIAS_CUENTAS["perdidas"], "Pérdidas")
    impuesto_renta = obtener_saldo_neto(CATEGORIAS_CUENTAS["impuesto_renta"], "Impuesto a la Renta")

    # 🔹 Obtener desglose de gastos operativos
    gastos_operativos = obtener_gastos_operativos()
    total_gastos_operativos = gastos_operativos["total_gastos_operativos"]

    # 🔹 Cálculos del Estado de Resultados
    utilidad_bruta = ventas_netas - costo_ventas
    utilidad_operativa = utilidad_bruta - total_gastos_operativos
    utilidad_antes_impuestos = utilidad_operativa + otros_ingresos - perdidas
    utilidad_neta = utilidad_antes_impuestos - impuesto_renta

    # 🔹 Imprimir cada cálculo paso a paso
    # print(f"\n📌 Utilidad Bruta: {utilidad_bruta} = Ventas Netas ({ventas_netas}) - Costo de Ventas ({costo_ventas})")
    # print(f"📌 Utilidad Operativa: {utilidad_operativa} = Utilidad Bruta ({utilidad_bruta}) - Gastos Operativos ({total_gastos_operativos})")
    # print(f"📌 Utilidad Antes de Impuestos: {utilidad_antes_impuestos} = Utilidad Operativa ({utilidad_operativa}) + Otros Ingresos ({otros_ingresos}) - Pérdidas ({perdidas})")
    # print(f"📌 Utilidad Neta: {utilidad_neta} = Utilidad Antes de Impuestos ({utilidad_antes_impuestos}) - Impuesto a la Renta ({impuesto_renta})")

    # 🔹 Construcción del JSON de salida
    resultado = {
        "ventas": ventas_netas,
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