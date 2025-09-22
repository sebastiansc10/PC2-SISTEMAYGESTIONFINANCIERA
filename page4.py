import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget,
    QMessageBox, QHeaderView, QComboBox, QDialog, QLabel, QLineEdit, QFormLayout
)
from app.funciones.DiarioTransaccion import mostrar_transacciones, obtener_cuentas, registrar_nueva_transaccion, eliminar_transaccion, actualizar_transaccion

class TransaccionDialog(QDialog):
    def __init__(self, parent=None, transaccion=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva Transacción" if transaccion is None else "Actualizar Transacción")
        self.transaccion = transaccion
        self.setup_ui()
        
    def setup_ui(self):
        layout = QFormLayout(self)

        # 🔹 Combobox para las cuentas
        self.cuenta_combo = QComboBox()
        self.cuenta_combo.setMinimumHeight(40)  # 🔹 Mayor altura para mejor legibilidad
        self.cuentas = obtener_cuentas()
        for id_cuenta, nombre in self.cuentas.items():
            self.cuenta_combo.addItem(f"{id_cuenta} - {nombre}", id_cuenta)

        # 🔹 Combobox para Debe/Haber
        self.dh_combo = QComboBox()
        self.dh_combo.setMinimumHeight(40)
        self.dh_combo.addItems(["Debe", "Haber"])

        # 🔹 Campo para la cantidad
        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("0.00")
        self.cantidad_input.setMinimumHeight(40)
        self.cantidad_input.setAlignment(QtCore.Qt.AlignRight)  # 🔹 Alineación a la derecha

        # 🔹 Agregar widgets al layout con iconos descriptivos
        layout.addRow("📌 <b>Cuenta:</b>", self.cuenta_combo)
        layout.addRow("💰 <b>Tipo:</b>", self.dh_combo)
        layout.addRow("📊 <b>Cantidad:</b>", self.cantidad_input)

        # 🔹 Botones de acción
        buttons = QHBoxLayout()
        self.btn_aceptar = QPushButton("💾 Guardar")
        self.btn_cancelar = QPushButton("❌ Cancelar")

        # 🔹 Aplicar estilo a los botones
        button_style = """
            QPushButton {
                background: #0078D7;
                color: white;
                padding: 16px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #444;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: #005A9E;
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: #004080;
                border: 2px solid #ffffff;
            }
        """
        self.btn_aceptar.setStyleSheet(button_style)

        cancel_button_style = """
            QPushButton {
                background: #e74c3c;
                color: white;
                padding: 16px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #444;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: #c0392b;
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: #a93226;
                border: 2px solid #ffffff;
            }
        """
        self.btn_cancelar.setStyleSheet(cancel_button_style)

        # 🔹 Añadir los botones al layout
        buttons.addWidget(self.btn_aceptar)
        buttons.addWidget(self.btn_cancelar)

        self.btn_aceptar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

        layout.addRow("", buttons)

        # 🔹 Si es una actualización, llenar los campos con los datos actuales
        if self.transaccion:
            index = self.cuenta_combo.findData(self.transaccion['id_cuenta'])
            self.cuenta_combo.setCurrentIndex(index)
            self.dh_combo.setCurrentText(self.transaccion['tipo'])
            self.cantidad_input.setText(str(self.transaccion['cantidad']))

        # 🔹 Aplicar estilo general a la ventana
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QComboBox, QLineEdit {
                background-color: #1a1a1a;
                color: white;
                border: 1px solid #444;
                padding: 10px;
                border-radius: 6px;
                font-size: 18px;
            }
            QComboBox::drop-down {
                width: 20px;
                subcontrol-origin: padding;
                subcontrol-position: right center;
            }
            QComboBox:hover, QLineEdit:hover {
                border: 1px solid #0078D7;
            }
            QComboBox:focus, QLineEdit:focus {
                border: 2px solid #0078D7;
                background-color: #222;
            }
        """)

        # 🔹 Activar el cursor de manito en los botones (forma correcta)
        self.btn_aceptar.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_cancelar.setCursor(QtCore.Qt.PointingHandCursor)
class Page4(QtWidgets.QWidget):
    def __init__(self, main_window, glosa, fecha, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.glosa = glosa
        self.fecha = fecha
        self.setup_ui()
        self.obtener_transacciones()

    def setup_ui(self):
        self.page4_layout = QVBoxLayout(self)
        
        # Título
        self.label = QtWidgets.QLabel(f"📜 Transacciones del Diario: {self.glosa}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 22px; font-weight: bold; color: #f1c40f; margin-bottom: 10px;")
        
        # Tabla
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Código de cuenta", "Nombre de cuenta", "Debe", "Haber"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)  # 🔹 Oculta los índices de fila
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            /* 🔹 Fondo General de la Tabla */
            QTableWidget {
                background-color: #121212;
                gridline-color: #444;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }

            /* 🔹 Ítems de la Tabla */
            QTableWidget::item {
                background-color: #1a1a1a;
                color: white;
                padding: 6px;
                border: none;  /* 🔹 Elimina el borde */
            }


            /* 🔹 Cabeceras */
            QHeaderView::section {
                background-color: #0078D7;
                color: white;
                padding: 10px;  
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 6px;  /* 🔹 Bordes redondeados */
            }

            /* 🔹 Selección de Items */
            QTableWidget::item:selected {
                background-color: #005A9E;
                color: white;
                border: 2px solid white;
                border-radius: 6px;  /* 🔹 Hace la selección más elegante */
            }

            /* 🔹 Estilo para el Scrollbar */
            QScrollBar:vertical {
                border: none;
                background: #1a1a1a;
                width: 12px; /* 🔹 Hace el scrollbar más delgado */
                margin: 2px 2px 2px 2px;
                border-radius: 6px;
            }

            /* 🔹 Parte del Scrollbar que se mueve */
            QScrollBar::handle:vertical {
                background: #444;
                border-radius: 6px;
                min-height: 20px;
            }
            
            /* 🔹 Cuando el cursor pasa sobre el Scroll */
            QScrollBar::handle:vertical:hover {
                background: #0078D7;
            }
            
            /* 🔹 Cuando se hace clic en el Scroll */
            QScrollBar::handle:vertical:pressed {
                background: #005A9E;
            }

            /* 🔹 Flechas del Scroll */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                width: 0px;
                height: 0px;
            }

            /* 🔹 Espacio entre scrollbar y bordes */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            /* 🔹 QDateEdit para que combine mejor */
            QDateEdit {
                background-color: #1a1a1a;
                color: white;
                font-weight: bold;
                border: none;
                padding: 6px 0px; /* 🔹 Ajuste vertical */
                font-size: 16px;
                text-align: center;
            }
            QDateEdit::drop-down {
                width: 20px;
                subcontrol-origin: padding;
                subcontrol-position: right center;
            }

            QDateEdit:hover {
                background-color: #2a2a2a;
                border: 1px solid #0078D7;
            }

            QDateEdit:focus {
                background-color: #005A9E;
                color: white;
                border: 2px solid #FFF;
            }
        """)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        self.btn_nueva_transaccion = self.create_button("➕ Nueva Transacción", "#4CAF50", "#45a049")
        self.btn_actualizar_transaccion = self.create_button("🔄 Actualizar Transacción", "#FFA500", "#cc8400")
        self.btn_borrar_transaccion = self.create_button("🗑️ Borrar Transacción", "#F44336", "#d32f2f")
        self.btn_back_diarios = self.create_button("🔙 Volver a Diarios", "#34495E", "#2c3e50")
        self.btn_back_home = self.create_button("🏠 Volver al Inicio", "#2C3E50", "#1a252f")
        
        # Conectar señales
        self.btn_nueva_transaccion.clicked.connect(self.mostrar_dialogo_nueva_transaccion)
        self.btn_actualizar_transaccion.clicked.connect(self.mostrar_dialogo_actualizar_transaccion)
        self.btn_borrar_transaccion.clicked.connect(self.borrar_transaccion_seleccionada)
        self.btn_back_diarios.clicked.connect(self.volver_a_diarios)
        self.btn_back_home.clicked.connect(self.volver_al_inicio)
        
        btn_layout.addWidget(self.btn_nueva_transaccion)
        btn_layout.addWidget(self.btn_actualizar_transaccion)
        btn_layout.addWidget(self.btn_borrar_transaccion)
        btn_layout.addWidget(self.btn_back_diarios)
        btn_layout.addWidget(self.btn_back_home)
        
        # Agregar widgets al layout principal
        self.page4_layout.addWidget(self.label)
        self.page4_layout.addWidget(self.tableWidget)
        self.page4_layout.addLayout(btn_layout)
        
        self.setLayout(self.page4_layout)

    def create_button(self, text, color, hover_color):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 18px 30px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #444;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 2px solid white;
            }}
            QPushButton:pressed {{
                background-color: #00000044;
                border: 2px solid #fff;
            }}
        """)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        button.setMinimumHeight(60)
        button.setFixedHeight(60)
        return button

    def mostrar_dialogo_nueva_transaccion(self):
        """Muestra el diálogo para agregar una nueva transacción."""
        dialogo = TransaccionDialog(self)
        if dialogo.exec_() == QDialog.Accepted:
            try:
                # Obtener datos del diálogo
                id_cuenta = dialogo.cuenta_combo.currentData()
                dh = dialogo.dh_combo.currentText()
                cantidad = float(dialogo.cantidad_input.text())

                # 🔹 Verificar si el código de cuenta ya existe en la tabla
                for row in range(self.tableWidget.rowCount()):
                    if self.tableWidget.item(row, 0).text() == str(id_cuenta):
                        QMessageBox.warning(self, "Error", "⚠️ El código de cuenta ya existe en la tabla.")
                        return  # 🔹 Detener el proceso de guardado

                # Registrar la transacción
                if registrar_nueva_transaccion(id_cuenta, dh, cantidad, self.glosa, self.fecha):
                    QMessageBox.information(self, "Éxito", "✅ Transacción registrada correctamente")
                    self.obtener_transacciones()  # 🔄 Actualizar la tabla
                else:
                    QMessageBox.warning(self, "Error", "❌ No se pudo registrar la transacción")
            except ValueError:
                QMessageBox.warning(self, "Error", "⚠️ Por favor ingrese una cantidad válida")

    def mostrar_dialogo_actualizar_transaccion(self):
        """Muestra el diálogo para actualizar una transacción existente."""
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "⚠️ Por favor, seleccione una transacción para actualizar.")
            return

        row = selected_items[0].row()
        id_cuenta_actual = self.tableWidget.item(row, 0).text()

        transaccion_actual = {
            'id_cuenta': id_cuenta_actual,
            'cuenta': self.tableWidget.item(row, 1).text(),
            'tipo': "Debe" if self.tableWidget.item(row, 2).text() != "0" else "Haber",
            'cantidad': float(self.tableWidget.item(row, 2).text() or self.tableWidget.item(row, 3).text())
        }

        dialogo = TransaccionDialog(self, transaccion_actual)
        if dialogo.exec_() == QDialog.Accepted:
            try:
                nueva_cuenta = dialogo.cuenta_combo.currentData()

                # 🔹 Validar si la nueva cuenta ya existe en otra fila (excepto en la actual)
                for r in range(self.tableWidget.rowCount()):
                    if r != row and self.tableWidget.item(r, 0).text() == str(nueva_cuenta):
                        QMessageBox.warning(self, "Error", "⚠️ No se pueden duplicar códigos de cuenta en la tabla.")
                        return  # 🔹 Detener el proceso de actualización

                nuevo_dh = dialogo.dh_combo.currentText()
                nueva_cantidad = float(dialogo.cantidad_input.text())

                resultado = json.loads(actualizar_transaccion(
                    self.glosa,
                    self.fecha,
                    transaccion_actual['id_cuenta'],
                    transaccion_actual['cantidad'],
                    transaccion_actual['tipo'],
                    nueva_cantidad,
                    nuevo_dh,
                    nueva_cuenta
                ))

                QMessageBox.information(self, "Resultado", resultado["mensaje"])
                self.obtener_transacciones()  # 🔄 Refrescar la tabla
            except ValueError:
                QMessageBox.warning(self, "Error", "⚠️ Por favor ingrese una cantidad válida")

    def borrar_transaccion_seleccionada(self):
        """Borra la transacción seleccionada en la tabla."""
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Por favor, seleccione una transacción para borrar.")
            return

        row = selected_items[0].row()
        id_cuenta = self.tableWidget.item(row, 0).text()
        
        cantidad = 0
        dh = ''
        for col in range(2, 4):
            valor = self.tableWidget.item(row, col).text()
            if valor != '0':
                cantidad = float(valor)
                dh = 'Debe' if col == 2 else 'Haber'
                break

        respuesta = QMessageBox.question(self, "Confirmar borrado", 
                                         "¿Está seguro de que desea borrar esta transacción?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            resultado = json.loads(eliminar_transaccion(self.glosa, self.fecha, id_cuenta, cantidad, dh))
            QMessageBox.information(self, "Resultado", resultado["mensaje"])
            self.obtener_transacciones()  # Actualizar la tabla

    def obtener_transacciones(self):
        """Obtiene las transacciones de un diario específico y las muestra en la tabla."""
        resultado_json = mostrar_transacciones(self.glosa, self.fecha)
        resultado = json.loads(resultado_json)
        self.tableWidget.setRowCount(len(resultado))
        
        for row, transaccion in enumerate(resultado):
            self.tableWidget.setRowHeight(row, 50)  # 🔹 Ajusta la altura de cada fila a 50px
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(transaccion["id_cuenta"])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(transaccion["cuenta"]))
            
            if transaccion["tipo"] == "Debe":
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(transaccion["cantidad"])))
                self.tableWidget.setItem(row, 3, QTableWidgetItem("0"))
            else:
                self.tableWidget.setItem(row, 2, QTableWidgetItem("0"))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(transaccion["cantidad"])))

    def volver_a_diarios(self):
        self.main_window.stackedWidget.setCurrentIndex(1)

    def volver_al_inicio(self):
        self.main_window.stackedWidget.setCurrentIndex(0)