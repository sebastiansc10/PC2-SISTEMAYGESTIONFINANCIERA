import json
from app.funciones.EstadoSituacion import calcularbalance  # Importamos la función que obtiene los datos

# Definimos la clasificación de cuentas por id_elemento
CATEGORIAS_CUENTAS = {
    "ventas": [7],  # Ingresos
    "costo_ventas": [6],  # Costos de venta
    "gastos_operativos": [6],  # Gastos operativos específicos
    "otros_ingresos": [7],  # Otros ingresos no operativos
    "perdidas": [6],  # Pérdidas extraordinarias
    "impuesto_renta": [8]  # Impuestos
}

def calcular_estado_resultados(fechainicio, fechafin):
    """
    Obtiene el Balance de Comprobación desde `calcularbalance` y genera el Estado de Resultados.
    """

    # Obtener datos del balance de comprobación como JSON
    balance_json = calcularbalance(fechainicio, fechafin)

    # Convertir JSON a lista de diccionarios
    balance = json.loads(balance_json)

    # Función para obtener valores dinámicamente por categoría
    def obtener_total_por_cuentas(lista_cuentas, tipo):
        """
        Obtiene el total de Debe o Haber según una lista de cuentas específicas.
        :param lista_cuentas: Lista de ID_Cuenta a considerar.
        :param tipo: 'Debe' o 'Haber'.
        :return: Suma total del tipo seleccionado.
        """
        return sum(item.get(tipo.lower(), 0) for item in balance if item["id_cuenta"] in lista_cuentas)

    # Función para obtener gastos operativos desglosados automáticamente
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

    # Obtener valores corregidos desde el Balance de Comprobación
    ventas = obtener_total_por_cuentas([70], "Haber")  # Solo cuenta de ventas
    costo_ventas = obtener_total_por_cuentas([69], "Debe")  # Solo costo de venta
    otros_ingresos = obtener_total_por_cuentas([75], "Haber")  # Solo otros ingresos
    perdidas = obtener_total_por_cuentas([66], "Debe")  # Solo pérdidas
    impuesto_renta = obtener_total_por_cuentas([88], "Debe")  # Solo impuesto a la renta

    # Obtener desglose de gastos operativos
    gastos_operativos = obtener_gastos_operativos()
    total_gastos_operativos = gastos_operativos["total_gastos_operativos"]

    # Cálculos del Estado de Resultados
    utilidad_bruta = ventas - costo_ventas
    utilidad_operativa = utilidad_bruta - total_gastos_operativos
    utilidad_antes_impuestos = utilidad_operativa + otros_ingresos - perdidas
    utilidad_neta = utilidad_antes_impuestos - impuesto_renta

    # Construcción del JSON de salida
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
