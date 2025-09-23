import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget,
    QMessageBox, QHeaderView, QComboBox, QDialog, QLabel, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QColor, QBrush
from app.funciones.DiarioTransaccion import (
    mostrar_transacciones, obtener_cuentas, registrar_nueva_transaccion,
    eliminar_transaccion, actualizar_transaccion
)

# ───────────────────────── Paleta StoneCo ─────────────────────────
STONE = {
    "bg":          "#0f1412",   # fondo app (oscuro elegante)
    "card":        "#151a18",
    "text":        "#ffffff",
    "muted":       "#cfe7d8",
    "g1":          "#00A859",   # primary
    "g2":          "#00C853",   # light
    "g_dark":      "#008C4A",   # hover/pressed
    "g_outline":   "#1a3c2d",   # bordes sutiles
    "accent":      "#1DE9B6",
    "danger":      "#e74c3c",
    "gray":        "#95a5a6",
    "gray_dark":   "#7f8c8d"
}

# ───────────────────────── Helpers de estilo ─────────────────────────
def stone_button(button: QPushButton, kind: str = "primary"):
    """Aplica estilo StoneCo al botón. kind: primary | secondary | danger"""
    if kind == "secondary":
        button.setStyleSheet(f"""
            QPushButton {{
                background: {STONE['gray_dark']};
                color: {STONE['text']};
                padding: 16px 24px;
                border-radius: 12px;
                border: 2px solid {STONE['g_outline']};
                font-size: 16px; font-weight: 800;
            }}
            QPushButton:hover {{
                background-color: {STONE['gray']};
                border: 2px solid {STONE['accent']};
            }}
            QPushButton:pressed {{
                background-color: #00000055;
                border: 2px solid #ffffff;
            }}
        """)
    elif kind == "danger":
        button.setStyleSheet(f"""
            QPushButton {{
                background: {STONE['danger']};
                color: {STONE['text']};
                padding: 16px 24px;
                border-radius: 12px;
                border: 2px solid {STONE['g_outline']};
                font-size: 16px; font-weight: 800;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
                border: 2px solid {STONE['accent']};
            }}
            QPushButton:pressed {{
                background-color: #00000055;
                border: 2px solid #ffffff;
            }}
        """)
    else:  # primary
        button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                         stop:0 {STONE['g1']}, stop:1 {STONE['g2']});
                color: {STONE['text']};
                padding: 16px 24px;
                border-radius: 12px;
                border: 2px solid {STONE['g_outline']};
                font-size: 16px; font-weight: 800;
            }}
            QPushButton:hover {{
                background-color: {STONE['g_dark']};
                border: 2px solid {STONE['accent']};
            }}
            QPushButton:pressed {{
                background-color: #00000055;
                border: 2px solid #ffffff;
            }}
        """)
    f = button.font(); f.setPointSize(16); f.setBold(True); button.setFont(f)
    button.setCursor(QtCore.Qt.PointingHandCursor)
    button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    button.setFixedHeight(56)

def stone_table(table: QTableWidget):
    table.setStyleSheet(f"""
        QTableWidget {{
            background-color: {STONE['card']};
            color: {STONE['text']};
            gridline-color: {STONE['g_outline']};
            border: 1px solid {STONE['g_outline']};
            border-radius: 10px;
        }}
        QHeaderView::section {{
            background-color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 {STONE['g1']}, stop:1 {STONE['g2']}
            );
            color: {STONE['text']};
            padding: 8px 10px;
            border: none;
            border-right: 1px solid {STONE['g_outline']};
            font-weight: 700;
        }}
        QTableWidget::item {{
            background-color: {STONE['card']};
            color: {STONE['text']};
            padding: 6px;
        }}
        QTableWidget::item:selected {{
            background-color: {STONE['g_dark']};
            color: {STONE['text']};
            border: 2px solid {STONE['accent']};
        }}
        QScrollBar:vertical {{
            border: none;
            background: {STONE['card']};
            width: 10px;
            margin: 2px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {STONE['g_outline']};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{ background: {STONE['g2']}; }}
        QScrollBar::handle:vertical:pressed {{ background: {STONE['g_dark']}; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ background: none; width:0; height:0; }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
    """)

# ───────────────────────── Diálogo de Transacción ─────────────────────────
class TransaccionDialog(QDialog):
    def __init__(self, parent=None, transaccion=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva Transacción" if transaccion is None else "Actualizar Transacción")
        self.transaccion = transaccion
        self.setup_ui()
        
    def setup_ui(self):
        layout = QFormLayout(self)

        # Combobox de cuentas
        self.cuenta_combo = QComboBox()
        self.cuenta_combo.setMinimumHeight(40)
        self.cuentas = obtener_cuentas()
        for id_cuenta, nombre in self.cuentas.items():
            self.cuenta_combo.addItem(f"{id_cuenta} - {nombre}", id_cuenta)

        # Debe/Haber
        self.dh_combo = QComboBox()
        self.dh_combo.setMinimumHeight(40)
        self.dh_combo.addItems(["Debe", "Haber"])

        # Cantidad
        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("0.00")
        self.cantidad_input.setMinimumHeight(40)
        self.cantidad_input.setAlignment(QtCore.Qt.AlignRight)

        # Campos
        layout.addRow("Cuenta:", self.cuenta_combo)
        layout.addRow("Tipo:", self.dh_combo)
        layout.addRow("Cantidad:", self.cantidad_input)

        # Botones
        buttons = QHBoxLayout()
        self.btn_aceptar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        stone_button(self.btn_aceptar, "primary")
        stone_button(self.btn_cancelar, "danger")
        self.btn_aceptar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)
        buttons.addWidget(self.btn_aceptar)
        buttons.addWidget(self.btn_cancelar)
        layout.addRow("", buttons)

        # Si es actualización, precargar
        if self.transaccion:
            index = self.cuenta_combo.findData(self.transaccion['id_cuenta'])
            if index >= 0:
                self.cuenta_combo.setCurrentIndex(index)
            self.dh_combo.setCurrentText(self.transaccion['tipo'])
            self.cantidad_input.setText(str(self.transaccion['cantidad']))

        # Estilo general StoneCo
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {STONE['bg']};
                color: {STONE['text']};
                border-radius: 12px;
                padding: 10px;
            }}
            QLabel {{
                color: {STONE['text']};
                font-size: 16px;
                font-weight: 700;
            }}
            QComboBox, QLineEdit {{
                background-color: {STONE['card']};
                color: {STONE['text']};
                border: 1px solid {STONE['g_outline']};
                padding: 10px;
                border-radius: 8px;
                font-size: 16px;
            }}
            QComboBox:hover, QLineEdit:hover {{
                border: 1px solid {STONE['g2']};
            }}
            QComboBox:focus, QLineEdit:focus {{
                border: 2px solid {STONE['accent']};
                background-color: {STONE['bg']};
            }}
        """)

# ───────────────────────── Página 4 (Transacciones) ─────────────────────────
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

        # Fondo
        self.setStyleSheet(f"background-color: {STONE['bg']}; color: {STONE['text']};")

        # Título (sin iconos)
        self.label = QtWidgets.QLabel(f"Transacciones del diario: {self.glosa}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {STONE['g2']}; margin-bottom: 10px;")

        # Tabla
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Código de cuenta", "Nombre de cuenta", "Debe", "Haber"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setAlternatingRowColors(False)
        stone_table(self.tableWidget)

        # Botones (sin iconos)
        btn_layout = QHBoxLayout()
        self.btn_nueva_transaccion      = QPushButton("Nueva transacción")
        self.btn_actualizar_transaccion = QPushButton("Actualizar transacción")
        self.btn_borrar_transaccion     = QPushButton("Borrar transacción")
        self.btn_back_diarios           = QPushButton("Volver a diarios")
        self.btn_back_home              = QPushButton("Volver al inicio")

        stone_button(self.btn_nueva_transaccion, "primary")
        stone_button(self.btn_actualizar_transaccion, "secondary")
        stone_button(self.btn_borrar_transaccion, "danger")
        stone_button(self.btn_back_diarios, "secondary")
        stone_button(self.btn_back_home, "secondary")

        # Conectar señales
        self.btn_nueva_transaccion.clicked.connect(self.mostrar_dialogo_nueva_transaccion)
        self.btn_actualizar_transaccion.clicked.connect(self.mostrar_dialogo_actualizar_transaccion)
        self.btn_borrar_transaccion.clicked.connect(self.borrar_transaccion_seleccionada)
        self.btn_back_diarios.clicked.connect(self.volver_a_diarios)
        self.btn_back_home.clicked.connect(self.volver_al_inicio)

        # Layout
        for b in (self.btn_nueva_transaccion, self.btn_actualizar_transaccion,
                  self.btn_borrar_transaccion, self.btn_back_diarios, self.btn_back_home):
            btn_layout.addWidget(b)

        self.page4_layout.addWidget(self.label)
        self.page4_layout.addWidget(self.tableWidget)
        self.page4_layout.addLayout(btn_layout)
        self.setLayout(self.page4_layout)

    # ─────────────────────── Acciones de UI ───────────────────────
    def mostrar_dialogo_nueva_transaccion(self):
        dialogo = TransaccionDialog(self)
        if dialogo.exec_() == QDialog.Accepted:
            try:
                id_cuenta = dialogo.cuenta_combo.currentData()
                dh = dialogo.dh_combo.currentText()
                cantidad = float(dialogo.cantidad_input.text())

                # Evitar duplicados de cuenta en la tabla
                for row in range(self.tableWidget.rowCount()):
                    if self.tableWidget.item(row, 0).text() == str(id_cuenta):
                        QMessageBox.warning(self, "Error", "El código de cuenta ya existe en la tabla.")
                        return

                if registrar_nueva_transaccion(id_cuenta, dh, cantidad, self.glosa, self.fecha):
                    QMessageBox.information(self, "Éxito", "Transacción registrada correctamente.")
                    self.obtener_transacciones()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo registrar la transacción.")
            except ValueError:
                QMessageBox.warning(self, "Error", "Ingrese una cantidad válida.")

    def mostrar_dialogo_actualizar_transaccion(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Seleccione una transacción para actualizar.")
            return

        row = selected_items[0].row()
        id_cuenta_actual = self.tableWidget.item(row, 0).text()

        # Detectar tipo y cantidad actuales
        tipo_actual = "Debe" if self.tableWidget.item(row, 2).text() != "0" else "Haber"
        cantidad_actual = float(self.tableWidget.item(row, 2).text() or self.tableWidget.item(row, 3).text())

        transaccion_actual = {
            'id_cuenta': id_cuenta_actual,
            'cuenta': self.tableWidget.item(row, 1).text(),
            'tipo': tipo_actual,
            'cantidad': cantidad_actual
        }

        dialogo = TransaccionDialog(self, transaccion_actual)
        if dialogo.exec_() == QDialog.Accepted:
            try:
                nueva_cuenta = dialogo.cuenta_combo.currentData()

                # Evitar duplicado de cuenta (salvo misma fila)
                for r in range(self.tableWidget.rowCount()):
                    if r != row and self.tableWidget.item(r, 0).text() == str(nueva_cuenta):
                        QMessageBox.warning(self, "Error", "No se pueden duplicar códigos de cuenta en la tabla.")
                        return

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

                QMessageBox.information(self, "Resultado", resultado.get("mensaje", "Actualización realizada."))
                self.obtener_transacciones()
            except ValueError:
                QMessageBox.warning(self, "Error", "Ingrese una cantidad válida.")

    def borrar_transaccion_seleccionada(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Seleccione una transacción para borrar.")
            return

        row = selected_items[0].row()
        id_cuenta = self.tableWidget.item(row, 0).text()

        # Detectar cantidad y tipo
        cantidad = 0.0
        dh = ''
        debe_val = self.tableWidget.item(row, 2).text()
        haber_val = self.tableWidget.item(row, 3).text()
        if debe_val and debe_val != '0':
            cantidad = float(debe_val); dh = 'Debe'
        else:
            cantidad = float(haber_val or 0); dh = 'Haber'

        respuesta = QMessageBox.question(
            self, "Confirmar borrado",
            "¿Está seguro de que desea borrar esta transacción?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            resultado = json.loads(eliminar_transaccion(self.glosa, self.fecha, id_cuenta, cantidad, dh))
            QMessageBox.information(self, "Resultado", resultado.get("mensaje", "Operación realizada."))
            self.obtener_transacciones()

    # ─────────────────────── Datos ───────────────────────
    def obtener_transacciones(self):
        resultado_json = mostrar_transacciones(self.glosa, self.fecha)
        resultado = json.loads(resultado_json)
        self.tableWidget.setRowCount(len(resultado))
        
        for row, transaccion in enumerate(resultado):
            self.tableWidget.setRowHeight(row, 50)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(transaccion["id_cuenta"])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(transaccion["cuenta"]))
            if transaccion["tipo"] == "Debe":
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(transaccion["cantidad"])))
                self.tableWidget.setItem(row, 3, QTableWidgetItem("0"))
            else:
                self.tableWidget.setItem(row, 2, QTableWidgetItem("0"))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(transaccion["cantidad"])))

    # ─────────────────────── Navegación ───────────────────────
    def volver_a_diarios(self):
        self.main_window.stackedWidget.setCurrentIndex(1)

    def volver_al_inicio(self):
        self.main_window.stackedWidget.setCurrentIndex(0)
