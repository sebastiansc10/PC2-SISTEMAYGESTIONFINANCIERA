import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget,
    QMessageBox, QHeaderView
)
from app.funciones.DiarioTransaccion import mostrar_transacciones

class Page4(QtWidgets.QWidget):
    def __init__(self, main_window, glosa, fecha, parent=None):
        """
        Página de Transacciones de un Diario Específico.
        :param main_window: Instancia de la ventana principal (para cambiar de página).
        :param glosa: Glosa del diario seleccionado.
        :param fecha: Fecha del diario seleccionado.
        """
        super().__init__(parent)
        self.main_window = main_window  # Referencia al main_window
        self.glosa = glosa
        self.fecha = fecha
        self.setup_ui()
        self.obtener_transacciones()

    def setup_ui(self):
        """Configura la interfaz gráfica de la página."""
        self.page4_layout = QVBoxLayout(self)

        # ✅ Título
        self.label = QtWidgets.QLabel(f"📜 Transacciones del Diario: {self.glosa}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        # ✅ Tabla de Transacciones
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

        # ✅ Botones de Acción
        self.btn_back_diarios = QPushButton("🔙 Volver a Diarios Registrados")
        self.btn_back_home = QPushButton("🏠 Volver al Inicio")
        
        self.btn_back_diarios.setStyleSheet("background-color: #34495E; color: white; padding: 8px; border-radius: 5px;")
        self.btn_back_home.setStyleSheet("background-color: #2C3E50; color: white; padding: 8px; border-radius: 5px;")

        # ✅ Conexión de los botones
        self.btn_back_diarios.clicked.connect(self.volver_a_diarios)
        self.btn_back_home.clicked.connect(self.volver_al_inicio)

        # ✅ Diseño de los botones
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_back_diarios)
        btn_layout.addWidget(self.btn_back_home)

        # ✅ Agregar widgets al layout
        self.page4_layout.addWidget(self.label)
        self.page4_layout.addWidget(self.tableWidget)
        self.page4_layout.addLayout(btn_layout)
        self.setLayout(self.page4_layout)

    def obtener_transacciones(self):
        """Obtiene las transacciones de un diario específico y las muestra en la tabla."""
        resultado_json = mostrar_transacciones(self.glosa, self.fecha)
        resultado = json.loads(resultado_json)
        self.tableWidget.setRowCount(len(resultado))
        
        for row, transaccion in enumerate(resultado):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(self.fecha))  # 📅 Fecha
            self.tableWidget.setItem(row, 1, QTableWidgetItem(transaccion["cuenta"]))  # 🏦 Cuenta
            
            if transaccion["tipo"] == "Debe":
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(transaccion["cantidad"])))  # 💰 Debe
                self.tableWidget.setItem(row, 3, QTableWidgetItem(""))  # 💳 Haber vacío
            else:
                self.tableWidget.setItem(row, 2, QTableWidgetItem(""))  # 💰 Debe vacío
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(transaccion["cantidad"])))  # 💳 Haber

    def volver_a_diarios(self):
        """Vuelve a la página de Diarios Registrados."""
        self.main_window.stackedWidget.setCurrentIndex(1)  # Cambia a `page2.py`

    def volver_al_inicio(self):
        """Vuelve a la página principal en el stackedWidget."""
        self.main_window.stackedWidget.setCurrentIndex(0)  # Cambia al inicio
