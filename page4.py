import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget,
    QMessageBox, QHeaderView, QComboBox, QDialog, QLabel, QLineEdit, QFormLayout
)
from app.funciones.DiarioTransaccion import mostrar_transacciones, obtener_cuentas, registrar_nueva_transaccion

class NuevaTransaccionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva Transacción")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Combobox para las cuentas
        self.cuenta_combo = QComboBox()
        self.cuentas = obtener_cuentas()
        for id_cuenta, nombre in self.cuentas.items():
            self.cuenta_combo.addItem(nombre, id_cuenta)
        
        # Combobox para Debe/Haber
        self.dh_combo = QComboBox()
        self.dh_combo.addItems(["Debe", "Haber"])
        
        # Campo para la cantidad
        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("0.00")
        
        # Agregar widgets al layout
        layout.addRow("Cuenta:", self.cuenta_combo)
        layout.addRow("Tipo:", self.dh_combo)
        layout.addRow("Cantidad:", self.cantidad_input)
        
        # Botones
        buttons = QHBoxLayout()
        self.btn_aceptar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        buttons.addWidget(self.btn_aceptar)
        buttons.addWidget(self.btn_cancelar)
        
        self.btn_aceptar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)
        
        layout.addRow("", buttons)

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
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        
        # Tabla
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["📅 Fecha", "🏦 Cuenta", "💰 Debe", "💳 Haber"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 5px;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #ccc;
            }
            QTableWidget::item:selected {
                background-color: #90CAF9;
                color: black;
            }
        """)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        self.btn_nueva_transaccion = QPushButton("➕ Nueva Transacción")
        self.btn_back_diarios = QPushButton("🔙 Volver a Diarios")
        self.btn_back_home = QPushButton("🏠 Volver al Inicio")
        
        self.btn_nueva_transaccion.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;"
        )
        self.btn_back_diarios.setStyleSheet(
            "background-color: #34495E; color: white; padding: 8px; border-radius: 5px;"
        )
        self.btn_back_home.setStyleSheet(
            "background-color: #2C3E50; color: white; padding: 8px; border-radius: 5px;"
        )
        
        # Conectar señales
        self.btn_nueva_transaccion.clicked.connect(self.mostrar_dialogo_nueva_transaccion)
        self.btn_back_diarios.clicked.connect(self.volver_a_diarios)
        self.btn_back_home.clicked.connect(self.volver_al_inicio)
        
        btn_layout.addWidget(self.btn_nueva_transaccion)
        btn_layout.addWidget(self.btn_back_diarios)
        btn_layout.addWidget(self.btn_back_home)
        
        # Agregar widgets al layout principal
        self.page4_layout.addWidget(self.label)
        self.page4_layout.addWidget(self.tableWidget)
        self.page4_layout.addLayout(btn_layout)
        
        self.setLayout(self.page4_layout)

    def mostrar_dialogo_nueva_transaccion(self):
        """Muestra el diálogo para agregar una nueva transacción."""
        dialogo = NuevaTransaccionDialog(self)
        if dialogo.exec_() == QDialog.Accepted:
            try:
                # Obtener datos del diálogo
                id_cuenta = dialogo.cuenta_combo.currentData()
                dh = dialogo.dh_combo.currentText()
                cantidad = float(dialogo.cantidad_input.text())
                
                # Registrar la transacción
                if registrar_nueva_transaccion(id_cuenta, dh, cantidad, self.glosa, self.fecha):
                    QMessageBox.information(self, "Éxito", "Transacción registrada correctamente")
                    self.obtener_transacciones()  # Actualizar la tabla
                else:
                    QMessageBox.warning(self, "Error", "No se pudo registrar la transacción")
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor ingrese una cantidad válida")

    def obtener_transacciones(self):
        """Obtiene las transacciones de un diario específico y las muestra en la tabla."""
        resultado_json = mostrar_transacciones(self.glosa, self.fecha)
        resultado = json.loads(resultado_json)
        self.tableWidget.setRowCount(len(resultado))
        
        for row, transaccion in enumerate(resultado):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(self.fecha))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(transaccion["cuenta"]))
            
            if transaccion["tipo"] == "Debe":
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(transaccion["cantidad"])))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(""))
            else:
                self.tableWidget.setItem(row, 2, QTableWidgetItem(""))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(transaccion["cantidad"])))

    def volver_a_diarios(self):
        self.main_window.stackedWidget.setCurrentIndex(1)

    def volver_al_inicio(self):
        self.main_window.stackedWidget.setCurrentIndex(0)