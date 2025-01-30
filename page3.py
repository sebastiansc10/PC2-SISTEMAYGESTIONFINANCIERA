import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QColor, QBrush
from app.funciones.EstadoSituacion import (
    calcularbalance, total_debe, total_haber, 
    situacion_activocorriente, situacion_totalactivocorriente,
    situacion_pasivo, situacion_totalpasivo,
    situacion_activonocorriente, situacion_totalactivonocorriente,
    situacion_patrimonio
)
from app.funciones.EstadoResultados import calcular_estado_resultados, utilidadantes
from app.funciones.DiarioTransaccion import diariotransaccion
from app.funciones.Mayorizar_BalanceComprobación import mayorizartransacciones

class Page3(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.diario_tables = []
        self.mayorizacion_tables = []
        self.setup_ui()

    def setup_ui(self):
        self.page3_layout = QVBoxLayout(self)
        
        # Set the background color of the entire page to black
        self.setStyleSheet("background-color: #000000; color: #ffffff;")

        # Update styles for title and subtitle
        self.titulo_principal = QtWidgets.QLabel("Registros contables")
        self.titulo_principal.setAlignment(QtCore.Qt.AlignCenter)
        self.titulo_principal.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffffff;
        """)

        self.subtitulo_fechas = QtWidgets.QLabel()
        self.subtitulo_fechas.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitulo_fechas.setStyleSheet("""
            font-size: 16px;
            margin-bottom: 20px;
            color: #ffffff;
        """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #000000;
                border: 1px solid #00CED1;
                border-radius: 10px;
            }
            QScrollBar:vertical {
                background-color: #000000;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #00CED1;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        content_widget = QtWidgets.QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Update styles for section titles
        titulo_style = """
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #00CED1;
        """

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

            if titulo == "Diarios y transacciones":
                self.diario_container = QtWidgets.QWidget()
                self.diario_layout = QVBoxLayout(self.diario_container)
                self.diario_layout.setSpacing(20)
                content_layout.addWidget(self.diario_container)
            elif titulo == "Mayorización":
                self.mayorizacion_container = QtWidgets.QWidget()
                self.mayorizacion_layout = QVBoxLayout(self.mayorizacion_container)
                self.mayorizacion_layout.setSpacing(20)
                content_layout.addWidget(self.mayorizacion_container)
            elif titulo == "Balanza de comprobación":
                self.tabla_balance = self.crear_tabla_generica(4, ["Código de cuenta", "Nombre de la cuenta", "Debe", "Haber"])
                content_layout.addWidget(self.tabla_balance)
            elif titulo == "Estado de situación financiera":
                tablas_layout = QHBoxLayout()
                
                columna_izquierda = QVBoxLayout()
                self.tabla_activo_corriente = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
                self.tabla_activo_no_corriente = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
                columna_izquierda.addWidget(self.tabla_activo_corriente)
                columna_izquierda.addWidget(self.tabla_activo_no_corriente)
                tablas_layout.addLayout(columna_izquierda)
                
                columna_derecha = QVBoxLayout()
                self.tabla_pasivos = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
                self.tabla_patrimonio = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
                columna_derecha.addWidget(self.tabla_pasivos)
                columna_derecha.addWidget(self.tabla_patrimonio)
                tablas_layout.addLayout(columna_derecha)
                
                content_layout.addLayout(tablas_layout)
                
                self.tabla_resumen = self.crear_tabla_generica(4, ["Activo total", "Valor", "Total pasivo + patrimonio", "Valor"])
                content_layout.addWidget(self.tabla_resumen)
            elif titulo == "Estado de resultados":
                self.tabla_resultados = self.crear_tabla_generica(3, ["Cuenta", "Monto", "Porcentaje del total"])
                # self.tabla_resultados.horizontalHeader().setVisible(False)
                content_layout.addWidget(self.tabla_resultados)

        self.scroll_area.setWidget(content_widget)

        self.page3_layout.addWidget(self.titulo_principal)
        self.page3_layout.addWidget(self.subtitulo_fechas)
        self.page3_layout.addWidget(self.scroll_area)

        self.boton_volver_inicio = QPushButton("🔙 Volver al Inicio")
        self.boton_volver_inicio.setStyleSheet("""
            background-color: #00CED1;
            color: #000000;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        """)
        self.boton_volver_inicio.clicked.connect(self.volver_al_inicio)
        
        self.page3_layout.addWidget(self.boton_volver_inicio)

        self.setLayout(self.page3_layout)

    def crear_tabla_generica(self, num_columnas, headers):
            tabla = QTableWidget()
            tabla.setColumnCount(num_columnas)
            tabla.setHorizontalHeaderLabels(headers)
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabla.verticalHeader().setVisible(False)
            tabla.setStyleSheet("""
                QTableWidget {
                    background-color: #000000;
                    color: #ffffff;  /* Color de la fuente en blanco */
                    border: 2px solid #00CED1;
                    border-radius: 4px;
                }
                QHeaderView::section {
                    background-color: #00CED1;
                    color: #000000;  /* Color de la fuente del encabezado en negro */
                    padding: 6px;
                    border: 1px solid #00CED1;
                    font-weight: bold;
                }
                QTableWidget::item:selected {
                    background-color: #00CED1;  /* Color de fondo cuando una celda está seleccionada */
                    color: #000000;  /* Color de texto cuando una celda está seleccionada */
                }
            """)
            tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            return tabla

    def crear_tabla(self):
        tabla = QTableWidget()
        tabla.setColumnCount(2)
        tabla.setHorizontalHeaderLabels(["Cuenta", "Saldo"])
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabla.verticalHeader().setVisible(False)
        tabla.setStyleSheet("""
            QTableWidget {
                background-color: #000000;
                color: #000000;
                border: 2px solid #00CED1;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #00CED1;
                color: #000000;
                padding: 6px;
                border: 1px solid #00CED1;
                font-weight: bold;
            }
            QTableWidget::item {
                border-bottom: 1px solid #00CED1;
            }
        """)
        return tabla

    def actualizar_fechas(self, fecha_inicio, fecha_fin):
        self.subtitulo_fechas.setText(f"Desde {fecha_inicio} hasta {fecha_fin}")
        self.actualizar_tabla_balance(fecha_inicio, fecha_fin)
        self.actualizar_tabla_resultados(fecha_inicio, fecha_fin)
        self.actualizar_tabla_activo_corriente(fecha_inicio, fecha_fin)
        self.actualizar_tabla_activo_no_corriente(fecha_inicio, fecha_fin)
        self.actualizar_tabla_pasivos(fecha_inicio, fecha_fin)
        self.actualizar_tabla_patrimonio(fecha_inicio, fecha_fin)
        self.actualizar_tabla_resumen(fecha_inicio, fecha_fin)
        self.actualizar_diarios(fecha_inicio, fecha_fin)
        self.actualizar_mayorizacion(fecha_inicio, fecha_fin)  # Add this line

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
        #color_total = QColor(255, 255, 200)  # Amarillo claro
        #debe_item.setBackground(QBrush(color_total))
        #haber_item.setBackground(QBrush(color_total))

        # Colorear la fila de total
        for col in range(2):
            item = self.tabla_balance.item(last_row, col)
            if item:
                item.setBackground(QBrush(QColor(255, 255, 200)))  # Fondo amarillo claro
                item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro

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
        datos_tabla = [
            ("Ventas", resultados_data["ventas"]),
            ("Costo de ventas", resultados_data["costo_ventas"]),
            ("Utilidad bruta", resultados_data["utilidad_bruta"]),
            ("Gastos de personal", resultados_data["Gastos de personal"]),
            ("Gastos de servicios", resultados_data["Gastos de servicios"]),
            ("Devaluación", resultados_data["Devaluación"]),
            ("Total gastos operativos", resultados_data["gastos_operativos"]),
            ("Utilidad operativa", resultados_data["utilidad_operativa"]),
            ("Otros ingresos", resultados_data["otros_ingresos"]),
            ("Pérdidas", resultados_data["perdidas"]),
            ("Utilidad antes de impuestos", resultados_data["utilidad_antes_impuestos"]),
            ("Impuesto a la renta", resultados_data["impuesto_renta"]),
            ("Utilidad neta", resultados_data["utilidad_neta"])
        ]

        # Filtrar filas en blanco
        datos_tabla = [fila for fila in datos_tabla if fila[1] != "" and fila[1] != 0]

        # Obtener el monto de "Ventas" como referencia para el 100%
        monto_ventas = next((monto for nombre, monto in datos_tabla if nombre == "Ventas"), 0)

        # Configurar la tabla
        self.tabla_resultados.setRowCount(len(datos_tabla))

        # Llenar la tabla con los datos
        for row, (nombre, valor) in enumerate(datos_tabla):
            self.agregar_fila_resultados(row, nombre, valor, monto_ventas)

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

    def actualizar_tabla_activo_corriente(self, fecha_inicio, fecha_fin):
        # Obtener los datos de activo corriente
        activo_corriente_json = situacion_activocorriente(fecha_inicio, fecha_fin)
        activo_corriente_data = json.loads(activo_corriente_json)
        
        # Configurar la tabla
        self.tabla_activo_corriente.setRowCount(len(activo_corriente_data) + 2)  # +2 para el encabezado y el total
        
        # Agregar el encabezado "Activo corriente"
        header_item = QTableWidgetItem("Activo corriente")
        header_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabla_activo_corriente.setSpan(0, 0, 1, 2)
        self.tabla_activo_corriente.setItem(0, 0, header_item)
        
        # Llenar la tabla con los datos
        for row, item in enumerate(activo_corriente_data, start=1):
            self.tabla_activo_corriente.setItem(row, 0, QTableWidgetItem(item['nombre_cuenta']))
            self.tabla_activo_corriente.setItem(row, 1, QTableWidgetItem(f"{item['saldo']:.2f}"))
        
        # Agregar la fila de total
        total_activo_corriente_json = situacion_totalactivocorriente(fecha_inicio, fecha_fin)
        total_activo_corriente = json.loads(total_activo_corriente_json)
        last_row = len(activo_corriente_data) + 1
        self.tabla_activo_corriente.setItem(last_row, 0, QTableWidgetItem("Total activo corriente"))
        self.tabla_activo_corriente.setItem(last_row, 1, QTableWidgetItem(f"{total_activo_corriente['Total_Saldo']:.2f}"))
        
        # Colorear la fila de total
        for col in range(2):
            item = self.tabla_activo_corriente.item(last_row, col)
            if item:
                item.setBackground(QBrush(QColor(255, 255, 200)))  # Fondo amarillo claro
                item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro
        
        # Ajustar el tamaño de las filas y columnas
        self.tabla_activo_corriente.resizeColumnsToContents()
        self.tabla_activo_corriente.resizeRowsToContents()
        
        # Deshabilitar la edición de la tabla
        self.tabla_activo_corriente.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Deshabilitar la barra de desplazamiento vertical
        self.tabla_activo_corriente.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Calcular y establecer la altura total de la tabla
        total_height = self.tabla_activo_corriente.horizontalHeader().height()
        for i in range(self.tabla_activo_corriente.rowCount()):
            total_height += self.tabla_activo_corriente.rowHeight(i)
        self.tabla_activo_corriente.setFixedHeight(total_height)

    def actualizar_tabla_activo_no_corriente(self, fecha_inicio, fecha_fin):
        # Obtener los datos de activo no corriente
        activo_no_corriente_json = situacion_activonocorriente(fecha_inicio, fecha_fin)
        activo_no_corriente_data = json.loads(activo_no_corriente_json)
        
        # Configurar la tabla
        self.tabla_activo_no_corriente.setRowCount(len(activo_no_corriente_data) + 2)  # +2 para el encabezado y el total
        
        # Agregar el encabezado "Activo no corriente"
        header_item = QTableWidgetItem("Activo no corriente")
        header_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabla_activo_no_corriente.setSpan(0, 0, 1, 2)
        self.tabla_activo_no_corriente.setItem(0, 0, header_item)
        
        # Llenar la tabla con los datos
        for row, item in enumerate(activo_no_corriente_data, start=1):
            self.tabla_activo_no_corriente.setItem(row, 0, QTableWidgetItem(item['nombre_cuenta']))
            self.tabla_activo_no_corriente.setItem(row, 1, QTableWidgetItem(f"{item['saldo']:.2f}"))
        
        # Agregar la fila de total
        total_activo_no_corriente_json = situacion_totalactivonocorriente(fecha_inicio, fecha_fin)
        total_activo_no_corriente = json.loads(total_activo_no_corriente_json)
        last_row = len(activo_no_corriente_data) + 1
        self.tabla_activo_no_corriente.setItem(last_row, 0, QTableWidgetItem("Total activo no corriente"))
        self.tabla_activo_no_corriente.setItem(last_row, 1, QTableWidgetItem(f"{total_activo_no_corriente['Total_Saldo']:.2f}"))
        
        # Colorear la fila de total
        # Colorear la fila de total
        for col in range(2):
            item = self.tabla_activo_no_corriente.item(last_row, col)
            if item:
                item.setBackground(QBrush(QColor(255, 255, 200)))  # Fondo amarillo claro
                item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro
        
        # Ajustar el tamaño de las filas y columnas
        self.tabla_activo_no_corriente.resizeColumnsToContents()
        self.tabla_activo_no_corriente.resizeRowsToContents()
        
        # Deshabilitar la edición de la tabla
        self.tabla_activo_no_corriente.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Deshabilitar la barra de desplazamiento vertical
        self.tabla_activo_no_corriente.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Calcular y establecer la altura total de la tabla
        total_height = self.tabla_activo_no_corriente.horizontalHeader().height()
        for i in range(self.tabla_activo_no_corriente.rowCount()):
            total_height += self.tabla_activo_no_corriente.rowHeight(i)
        self.tabla_activo_no_corriente.setFixedHeight(total_height)

    def actualizar_tabla_pasivos(self, fecha_inicio, fecha_fin):
        # Obtener los datos de pasivos
        pasivos_json = situacion_pasivo(fecha_inicio, fecha_fin)
        pasivos_data = json.loads(pasivos_json)
        
        # Configurar la tabla
        self.tabla_pasivos.setRowCount(len(pasivos_data) + 2)  # +2 para el encabezado y el total
        
        # Agregar el encabezado "Pasivos"
        header_item = QTableWidgetItem("Pasivos")
        header_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabla_pasivos.setSpan(0, 0, 1, 2)
        self.tabla_pasivos.setItem(0, 0, header_item)
        
        # Llenar la tabla con los datos
        for row, item in enumerate(pasivos_data, start=1):
            self.tabla_pasivos.setItem(row, 0, QTableWidgetItem(item['nombre_cuenta']))
            self.tabla_pasivos.setItem(row, 1, QTableWidgetItem(f"{item['saldo']:.2f}"))
        
        # Agregar la fila de total
        total_pasivos_json = situacion_totalpasivo(fecha_inicio, fecha_fin)
        total_pasivos = json.loads(total_pasivos_json)
        last_row = len(pasivos_data) + 1
        self.tabla_pasivos.setItem(last_row, 0, QTableWidgetItem("Total pasivos"))
        self.tabla_pasivos.setItem(last_row, 1, QTableWidgetItem(f"{total_pasivos['Total_Saldo']:.2f}"))
        
        # Colorear la fila de total
# Colorear la fila de total
        for col in range(2):
            item = self.tabla_pasivos.item(last_row, col)
            if item:
                item.setBackground(QBrush(QColor(255, 255, 200)))  # Fondo amarillo claro
                item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro
        
        # Ajustar el tamaño de las filas y columnas
        self.tabla_pasivos.resizeColumnsToContents()
        self.tabla_pasivos.resizeRowsToContents()
        
        # Deshabilitar la edición de la tabla
        self.tabla_pasivos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Deshabilitar la barra de desplazamiento vertical
        self.tabla_pasivos.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Calcular y establecer la altura total de la tabla
        total_height = self.tabla_pasivos.horizontalHeader().height()
        for i in range(self.tabla_pasivos.rowCount()):
            total_height += self.tabla_pasivos.rowHeight(i)
        self.tabla_pasivos.setFixedHeight(total_height)

    def actualizar_tabla_patrimonio(self, fecha_inicio, fecha_fin):
        # Obtener los datos de patrimonio
        patrimonio_json = situacion_patrimonio(fecha_inicio, fecha_fin)
        patrimonio_data = json.loads(patrimonio_json)
        
        # Obtener utilidades acumuladas
        utilidad_acumulada_json = utilidadantes(fecha_inicio, fecha_fin)
        utilidad_acumulada = json.loads(utilidad_acumulada_json)['utilidad_antes_impuestos']
        
        # Configurar la tabla
        self.tabla_patrimonio.setRowCount(len(patrimonio_data) + 3)  # +3 para el encabezado, utilidades acumuladas y total
        
        # Agregar el encabezado "Patrimonio"
        header_item = QTableWidgetItem("Patrimonio")
        header_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tabla_patrimonio.setSpan(0, 0, 1, 2)
        self.tabla_patrimonio.setItem(0, 0, header_item)
        
        # Llenar la tabla con los datos
        total_patrimonio = 0
        for row, item in enumerate(patrimonio_data, start=1):
            self.tabla_patrimonio.setItem(row, 0, QTableWidgetItem(item['nombre_cuenta']))
            self.tabla_patrimonio.setItem(row, 1, QTableWidgetItem(f"{item['saldo']:.2f}"))
            total_patrimonio += item['saldo']
        
        # Agregar fila de utilidades acumuladas
        row = len(patrimonio_data) + 1
        self.tabla_patrimonio.setItem(row, 0, QTableWidgetItem("Utilidades acumuladas"))
        self.tabla_patrimonio.setItem(row, 1, QTableWidgetItem(f"{utilidad_acumulada:.2f}"))
                
        # Colorear la fila de utilidades acumuladas
        for col in range(2):
            item = self.tabla_patrimonio.item(row, col)
            if item:
                item.setBackground(QBrush(QColor(255, 200, 100)))  # Fondo naranja
                item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro
        
        total_patrimonio += utilidad_acumulada
        
        # Agregar fila de total patrimonio
        row = len(patrimonio_data) + 2
        self.tabla_patrimonio.setItem(row, 0, QTableWidgetItem("Total patrimonio"))
        self.tabla_patrimonio.setItem(row, 1, QTableWidgetItem(f"{total_patrimonio:.2f}"))
        
        # Colorear la fila de total patrimonio de amarillo claro
        for col in range(2):
            item = self.tabla_patrimonio.item(row, col)
            if item:
                item.setBackground(QBrush(QColor(255, 255, 200)))  # Fondo amarillo claro
                item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro
        
        # Ajustar el tamaño de las filas y columnas
        self.tabla_patrimonio.resizeColumnsToContents()
        self.tabla_patrimonio.resizeRowsToContents()
        
        # Deshabilitar la edición de la tabla
        self.tabla_patrimonio.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Deshabilitar la barra de desplazamiento vertical
        self.tabla_patrimonio.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Calcular y establecer la altura total de la tabla
        total_height = self.tabla_patrimonio.horizontalHeader().height()
        for i in range(self.tabla_patrimonio.rowCount()):
            total_height += self.tabla_patrimonio.rowHeight(i)
        self.tabla_patrimonio.setFixedHeight(total_height)

    def agregar_fila_resultados(self, row, nombre, valor, monto_ventas):
        # Columna 1: Nombre de la cuenta
        item_nombre = QTableWidgetItem(nombre)
        item_nombre.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.tabla_resultados.setItem(row, 0, item_nombre)

        # Columna 2: Monto
        if isinstance(valor, (int, float)):
            item_valor = QTableWidgetItem(f"{valor:.2f}")
        else:
            item_valor = QTableWidgetItem(str(valor))
        item_valor.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_resultados.setItem(row, 1, item_valor)

        # Columna 3: Porcentaje del total
        if monto_ventas != 0:  # Evitar división por cero
            porcentaje = (valor / monto_ventas) * 100
        else:
            porcentaje = 0
        item_porcentaje = QTableWidgetItem(f"{porcentaje:.2f}%")
        item_porcentaje.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tabla_resultados.setItem(row, 2, item_porcentaje)

    # Asegúrate de que el método colorear_fila también establezca el texto en negro
    def colorear_fila(self, nombre_fila, color):
        for row in range(self.tabla_resultados.rowCount()):
            if self.tabla_resultados.item(row, 0).text() == nombre_fila:
                for col in range(self.tabla_resultados.columnCount()):
                    item = self.tabla_resultados.item(row, col)
                    if item:
                        item.setBackground(QBrush(color))
                        item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro
                break


    def actualizar_tabla_resumen(self, fecha_inicio, fecha_fin):
        # Obtener los totales necesarios
        total_activo_corriente = json.loads(situacion_totalactivocorriente(fecha_inicio, fecha_fin))['Total_Saldo']
        total_activo_no_corriente = json.loads(situacion_totalactivonocorriente(fecha_inicio, fecha_fin))['Total_Saldo']
        total_pasivo = json.loads(situacion_totalpasivo(fecha_inicio, fecha_fin))['Total_Saldo']
        
        # Calcular el patrimonio total (incluyendo utilidades acumuladas)
        patrimonio_data = json.loads(situacion_patrimonio(fecha_inicio, fecha_fin))
        utilidad_acumulada = json.loads(utilidadantes(fecha_inicio, fecha_fin))['utilidad_antes_impuestos']
        total_patrimonio = sum(item['saldo'] for item in patrimonio_data) + utilidad_acumulada

        # Calcular los totales
        activo_total = total_activo_corriente + total_activo_no_corriente
        pasivo_patrimonio_total = total_pasivo + total_patrimonio

        # Configurar la tabla con una fila
        self.tabla_resumen.setRowCount(1)  # Asegurar que la tabla tenga al menos una fila

        # Llenar la tabla con los datos
        self.tabla_resumen.setItem(0, 0, QTableWidgetItem("Activo total"))
        self.tabla_resumen.setItem(0, 1, QTableWidgetItem(f"{activo_total:.2f}"))
        self.tabla_resumen.setItem(0, 2, QTableWidgetItem("Total pasivo + patrimonio"))
        self.tabla_resumen.setItem(0, 3, QTableWidgetItem(f"{pasivo_patrimonio_total:.2f}"))

        # Colorear la fila de total
        for col in range(4):  # 4 columnas en la tabla
            item = self.tabla_resumen.item(0, col)
            if item:
                item.setBackground(QBrush(QColor(0, 255, 0)))  # Fondo verde
                item.setForeground(QBrush(QColor(0, 0, 0)))  # Texto en negro

        # Ajustar el tamaño de las filas y columnas
        self.tabla_resumen.resizeColumnsToContents()
        self.tabla_resumen.resizeRowsToContents()

        # Deshabilitar la edición de la tabla
        self.tabla_resumen.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Calcular y establecer la altura total de la tabla
        total_height = self.tabla_resumen.horizontalHeader().height() + self.tabla_resumen.rowHeight(0)
        self.tabla_resumen.setFixedHeight(total_height)


    def crear_tabla_diario(self):
        """Create a new table for diario entries"""
        tabla = QTableWidget()
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels([
            "Código de cuenta",
            "Nombre de cuenta",
            "Debe",
            "Haber"
        ])
        # Remove row numbers
        tabla.verticalHeader().setVisible(False)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabla.setStyleSheet("""
            QTableWidget {
                background-color: #000000;
                color: #ffffff;  /* Color de la fuente en blanco */
                border: 2px solid #00CED1;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #00CED1;
                color: #000000;  /* Color de la fuente del encabezado en negro */
                padding: 6px;
                border: 1px solid #00CED1;
                font-weight: bold;
            }
            QTableWidget::item {
                border-bottom: 1px solid #00CED1;
                color: #ffffff;  /* Color de la fuente en blanco */
            }
        """)
        tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        return tabla


    def actualizar_diarios(self, fecha_inicio, fecha_fin):
        """Actualiza las tablas de diario eliminando duplicaciones antes de insertar nuevos datos."""
        # 💡 Limpiar los widgets existentes antes de agregar nuevos
        while self.diario_layout.count():
            item = self.diario_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Obtener los datos de los diarios
        diarios_json = diariotransaccion(fecha_inicio, fecha_fin)
        diarios_data = json.loads(diarios_json)

        # Crear nuevas tablas para cada diario
        for diario in diarios_data:
            # Crear el encabezado con la fecha
            fecha_label = QtWidgets.QLabel(diario['fecha'])
            fecha_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
            self.diario_layout.addWidget(fecha_label)

            # Crear la tabla
            tabla = self.crear_tabla_diario()
            tabla.setRowCount(len(diario['transacciones']))

            # Poblar la tabla con transacciones
            for row, trans in enumerate(diario['transacciones']):
                tabla.setItem(row, 0, QTableWidgetItem(str(trans['id_cuenta'])))
                tabla.setItem(row, 1, QTableWidgetItem(trans['nombre_cuenta']))

                if trans['dh'] == 'Debe':
                    tabla.setItem(row, 2, QTableWidgetItem(f"{trans['cantidad']:.2f}"))
                    tabla.setItem(row, 3, QTableWidgetItem("0.00"))
                else:
                    tabla.setItem(row, 2, QTableWidgetItem("0.00"))
                    tabla.setItem(row, 3, QTableWidgetItem(f"{trans['cantidad']:.2f}"))

            # Ajustar altura de la tabla
            tabla.resizeRowsToContents()
            total_height = tabla.horizontalHeader().height()
            for i in range(tabla.rowCount()):
                total_height += tabla.rowHeight(i)
            tabla.setFixedHeight(total_height)
            tabla.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            # Agregar la tabla al layout
            self.diario_layout.addWidget(tabla)

            # Agregar la glosa
            glosa_label = QtWidgets.QLabel(f"Glosa: {diario['glosa']}")
            glosa_label.setStyleSheet("font-style: italic; padding: 5px; color: #ffffff;")
            self.diario_layout.addWidget(glosa_label)

            # Agregar un espacio entre registros
            self.diario_layout.addSpacing(10)

            # Guardar referencia a la tabla
            self.diario_tables.append(tabla)

    def crear_tabla_mayorizacion(self, id_cuenta, nombre_cuenta):
        """Create a new table for mayorizacion entries"""
        tabla = QTableWidget()
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels([
            "Fecha",
            "Debe",
            "Haber"
        ])
        
        # Set the table title with updated style
        title_label = QtWidgets.QLabel(f"{id_cuenta} - {nombre_cuenta}")
        title_label.setStyleSheet("""
            color: #00CED1;
            font-weight: bold;
            font-size: 14px;
            padding: 5px;
        """)
        self.mayorizacion_layout.addWidget(title_label)
        
        # Remove row numbers
        tabla.verticalHeader().setVisible(False)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabla.setStyleSheet("""
            QTableWidget {
                background-color: #000000;
                color: #ffffff;  /* Color de la fuente en blanco */
                border: 2px solid #00CED1;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #00CED1;
                color: #000000;  /* Color de la fuente del encabezado en negro */
                padding: 6px;
                border: 1px solid #00CED1;
                font-weight: bold;
            }
            QTableWidget::item {
                border-bottom: 1px solid #00CED1;
                color: #ffffff;  /* Color de la fuente en blanco */
            }
        """)
        tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        return tabla


    def actualizar_mayorizacion(self, fecha_inicio, fecha_fin):
        """Actualiza las tablas de mayorización eliminando duplicaciones antes de insertar nuevos datos."""
        # 💡 Limpiar los widgets existentes antes de agregar nuevos
        while self.mayorizacion_layout.count():
            item = self.mayorizacion_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Obtener los datos de mayorización
        mayorizacion_json = mayorizartransacciones(fecha_inicio, fecha_fin)
        mayorizacion_data = json.loads(mayorizacion_json)

        # Agrupar las transacciones por cuenta
        cuentas = {}
        for trans in mayorizacion_data:
            key = (trans['id_cuenta'], trans['nombre_cuenta'])
            if key not in cuentas:
                cuentas[key] = []
            cuentas[key].append(trans)

        # Crear nuevas tablas para cada cuenta
        for (id_cuenta, nombre_cuenta), transacciones in cuentas.items():
            # Crear la tabla
            tabla = self.crear_tabla_mayorizacion(id_cuenta, nombre_cuenta)
            tabla.setRowCount(len(transacciones) + 1)  # +1 para la fila de saldo

            # Poblar la tabla con transacciones
            total_debe = 0
            total_haber = 0
            for row, trans in enumerate(transacciones):
                tabla.setItem(row, 0, QTableWidgetItem(trans['fecha']))
                
                if trans['dh'] == 'Debe':
                    tabla.setItem(row, 1, QTableWidgetItem(f"{trans['cantidad']:.2f}"))
                    tabla.setItem(row, 2, QTableWidgetItem("0.00"))
                    total_debe += trans['cantidad']
                else:
                    tabla.setItem(row, 1, QTableWidgetItem("0.00"))
                    tabla.setItem(row, 2, QTableWidgetItem(f"{trans['cantidad']:.2f}"))
                    total_haber += trans['cantidad']

            # Calcular y agregar la fila de saldo
            last_row = len(transacciones)
            saldo = total_debe - total_haber
            saldo_item = QTableWidgetItem("Saldo")
            saldo_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            tabla.setItem(last_row, 0, saldo_item)

            if saldo >= 0:
                tabla.setItem(last_row, 1, QTableWidgetItem(f"{abs(saldo):.2f}"))
                tabla.setItem(last_row, 2, QTableWidgetItem("0.00"))
            else:
                tabla.setItem(last_row, 1, QTableWidgetItem("0.00"))
                tabla.setItem(last_row, 2, QTableWidgetItem(f"{abs(saldo):.2f}"))

            # Ajustar altura de la tabla
            tabla.resizeRowsToContents()
            total_height = tabla.horizontalHeader().height()
            for i in range(tabla.rowCount()):
                total_height += tabla.rowHeight(i)
            tabla.setFixedHeight(total_height)
            tabla.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            # Agregar la tabla al layout
            self.mayorizacion_layout.addWidget(tabla)

            # Agregar espacio entre cuentas
            self.mayorizacion_layout.addSpacing(20)

            # Guardar referencia a la tabla
            self.mayorizacion_tables.append(tabla)

    def closeEvent(self, event):
        # Clear diario tables
        for tabla in self.diario_tables:
            self.diario_layout.removeWidget(tabla)
            tabla.deleteLater()
        self.diario_tables.clear()
        
        # Clear mayorizacion tables
        for tabla in self.mayorizacion_tables:
            self.mayorizacion_layout.removeWidget(tabla)
            tabla.deleteLater()
        self.mayorizacion_tables.clear()
        
        event.accept()

    def volver_al_inicio(self):
        """Regresa a la página principal."""
        if self.parent_window:
            self.parent_window.stackedWidget.setCurrentIndex(0)