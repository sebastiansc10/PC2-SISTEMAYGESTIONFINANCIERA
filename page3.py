import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QColor, QBrush
from app.funciones.EstadoSituacion import calcularbalance, total_debe, total_haber
from app.funciones.EstadoResultados import calcular_estado_resultados

class Page3(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.page3_layout = QVBoxLayout(self)

        # Título principal (fuera del área de desplazamiento)
        self.titulo_principal = QtWidgets.QLabel("Registros contables")
        self.titulo_principal.setAlignment(QtCore.Qt.AlignCenter)
        self.titulo_principal.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #2C3E50;
    """)

        # Subtítulo con fechas (fuera del área de desplazamiento)
        self.subtitulo_fechas = QtWidgets.QLabel()
        self.subtitulo_fechas.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitulo_fechas.setStyleSheet("""
        font-size: 16px;
        margin-bottom: 20px;
        color: #34495E;
    """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 10px;
    """)

        content_widget = QtWidgets.QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Estilos para los títulos dentro del área de desplazamiento
        titulo_style = """
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        color: #2980B9;
        """

        # Agregar los nuevos títulos y contenido de ejemplo
        titulos = [
            "Diarios y transacciones",
            "Mayorización",
            "Balanza de comprobación",
            "Estado de situación financiera",
            "Estado de resultados"
        ]

        for titulo in titulos:
            label_titulo = QtWidgets.QLabel(titulo)
            label_titulo.setStyleSheet(titulo_style)
            content_layout.addWidget(label_titulo)

            if titulo == "Balanza de comprobación":
                # Crear la tabla de balance de comprobación
                self.tabla_balance = QTableWidget()
                self.tabla_balance.setColumnCount(4)
                self.tabla_balance.setHorizontalHeaderLabels(["Código de cuenta", "Nombre de la cuenta", "Debe", "Haber"])
                self.tabla_balance.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.tabla_balance.setStyleSheet("""
                    QTableWidget {
                        border: none;
                    }
                    QHeaderView::section {
                        background-color: #f0f0f0;
                        padding: 4px;
                        border: 1px solid #d0d0d0;
                        font-weight: bold;
                    }
                """)
                content_layout.addWidget(self.tabla_balance)
            elif titulo == "Estado de resultados":
                # Crear la tabla de estado de resultados
                self.tabla_resultados = QTableWidget()
                self.tabla_resultados.setColumnCount(2)
                self.tabla_resultados.setHorizontalHeaderLabels(["", ""])
                self.tabla_resultados.horizontalHeader().setVisible(False)
                self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.tabla_resultados.setStyleSheet("""
                    QTableWidget {
                        border: none;
                    }
                """)
                content_layout.addWidget(self.tabla_resultados)
            else:
                # Agregar contenido de ejemplo para otras secciones
                for i in range(5):
                    label = QtWidgets.QLabel(f"Registro de {titulo.lower()} {i + 1}")
                    label.setStyleSheet("font-size: 16px; padding: 10px;")
                    content_layout.addWidget(label)

        self.scroll_area.setWidget(content_widget)

        self.page3_layout.addWidget(self.titulo_principal)
        self.page3_layout.addWidget(self.subtitulo_fechas)
        self.page3_layout.addWidget(self.scroll_area)
        self.setLayout(self.page3_layout)

    def actualizar_fechas(self, fecha_inicio, fecha_fin):
        self.subtitulo_fechas.setText(f"Desde {fecha_inicio} hasta {fecha_fin}")
        self.actualizar_tabla_balance(fecha_inicio, fecha_fin)
        self.actualizar_tabla_resultados(fecha_inicio, fecha_fin)

    def actualizar_tabla_balance(self, fecha_inicio, fecha_fin):
        # Aquí llamamos a la función calcularbalance
        balance_json = calcularbalance(fecha_inicio, fecha_fin)
        balance_data = json.loads(balance_json)

        # Configurar la tabla
        self.tabla_balance.setRowCount(len(balance_data) + 1)  # +1 para la fila de total

        # Llenar la tabla con los datos
        for row, item in enumerate(balance_data):
            self.tabla_balance.setItem(row, 0, QTableWidgetItem(str(item['id_cuenta'])))
            self.tabla_balance.setItem(row, 1, QTableWidgetItem(item['nombre_cuenta']))
            self.tabla_balance.setItem(row, 2, QTableWidgetItem(f"{item['debe']:.2f}"))
            self.tabla_balance.setItem(row, 3, QTableWidgetItem(f"{item['haber']:.2f}"))

        # Agregar la fila de total
        last_row = len(balance_data)
        self.tabla_balance.setSpan(last_row, 0, 1, 2)  # Fusionar las dos primeras columnas
        total_item = QTableWidgetItem("Total:")
        total_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_balance.setItem(last_row, 0, total_item)

        # Obtener y mostrar los totales
        total_debe_valor = total_debe(fecha_inicio, fecha_fin)
        total_haber_valor = total_haber(fecha_inicio, fecha_fin)

        debe_item = QTableWidgetItem(f"{total_debe_valor:.2f}")
        haber_item = QTableWidgetItem(f"{total_haber_valor:.2f}")

        # Establecer el color de fondo para las celdas de total
        color_total = QColor(255, 255, 200)  # Amarillo claro
        debe_item.setBackground(QBrush(color_total))
        haber_item.setBackground(QBrush(color_total))

        self.tabla_balance.setItem(last_row, 2, debe_item)
        self.tabla_balance.setItem(last_row, 3, haber_item)

        # Ajustar el tamaño de las filas y columnas
        self.tabla_balance.resizeColumnsToContents()
        self.tabla_balance.resizeRowsToContents()

        # Calcular y establecer la altura total de la tabla
        total_height = self.tabla_balance.horizontalHeader().height()
        for i in range(self.tabla_balance.rowCount()):
            total_height += self.tabla_balance.rowHeight(i)

        # Establecer la altura fija de la tabla
        self.tabla_balance.setFixedHeight(total_height)
        
        self.tabla_balance.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Deshabilitar la barra de desplazamiento vertical
        self.tabla_balance.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def actualizar_tabla_resultados(self, fecha_inicio, fecha_fin):
        # Llamar a la función calcular_estado_resultados
        resultados_json = calcular_estado_resultados(fecha_inicio, fecha_fin)
        resultados_data = json.loads(resultados_json)

        # Preparar los datos para la tabla
        datos_tabla = []
        datos_tabla.append(("Ventas", resultados_data["ventas"]))
        datos_tabla.append(("Costo de ventas", resultados_data["costo_ventas"]))
        datos_tabla.append(("Utilidad bruta", resultados_data["utilidad_bruta"]))
        datos_tabla.append(("Gastos operativos", ""))
        for gasto, valor in resultados_data["gastos_operativos"]["detalle"].items():
            datos_tabla.append((f"  {gasto}", valor))
        datos_tabla.append(("Total gastos operativos", resultados_data["gastos_operativos"]["total_gastos_operativos"]))
        datos_tabla.append(("Utilidad operativa", resultados_data["utilidad_operativa"]))
        datos_tabla.append(("Otros ingresos", resultados_data["otros_ingresos"]))
        datos_tabla.append(("Pérdidas", resultados_data["perdidas"]))
        datos_tabla.append(("Utilidad antes de impuestos", resultados_data["utilidad_antes_impuestos"]))
        datos_tabla.append(("Impuesto a la renta", resultados_data["impuesto_renta"]))
        datos_tabla.append(("Utilidad neta", resultados_data["utilidad_neta"]))

        # Filtrar filas en blanco
        datos_tabla = [fila for fila in datos_tabla if fila[1] != "" and fila[1] != 0]

        # Configurar la tabla
        self.tabla_resultados.setRowCount(len(datos_tabla))

        # Llenar la tabla con los datos
        for row, (nombre, valor) in enumerate(datos_tabla):
            self.agregar_fila_resultados(row, nombre, valor)

        # Colorear filas específicas
        self.colorear_fila("Utilidad bruta", QColor(255, 255, 200))
        self.colorear_fila("Utilidad operativa", QColor(255, 255, 200))
        self.colorear_fila("Utilidad antes de impuestos", QColor(255, 200, 100))

        # Ajustar el tamaño de las filas y columnas
        self.tabla_resultados.resizeColumnsToContents()
        self.tabla_resultados.resizeRowsToContents()

        # Calcular y establecer la altura total de la tabla
        total_height = self.tabla_resultados.horizontalHeader().height()
        for i in range(self.tabla_resultados.rowCount()):
            total_height += self.tabla_resultados.rowHeight(i)

        # Establecer la altura fija de la tabla
        self.tabla_resultados.setFixedHeight(total_height)

        self.tabla_resultados.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Deshabilitar la barra de desplazamiento vertical
        self.tabla_resultados.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def agregar_fila_resultados(self, row, nombre, valor):
        item_nombre = QTableWidgetItem(nombre)
        item_nombre.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.tabla_resultados.setItem(row, 0, item_nombre)

        if isinstance(valor, (int, float)):
            item_valor = QTableWidgetItem(f"{valor:.2f}")
        else:
            item_valor = QTableWidgetItem(str(valor))
        item_valor.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_resultados.setItem(row, 1, item_valor)

    def colorear_fila(self, nombre_fila, color):
        for row in range(self.tabla_resultados.rowCount()):
            if self.tabla_resultados.item(row, 0).text() == nombre_fila:
                for col in range(self.tabla_resultados.columnCount()):
                    self.tabla_resultados.item(row, col).setBackground(QBrush(color))
                break

