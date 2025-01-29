import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from app.funciones.EstadoSituacion import calcularbalance

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

    def actualizar_tabla_balance(self, fecha_inicio, fecha_fin):
        # Aquí llamamos a la función calcularbalance
        balance_json = calcularbalance(fecha_inicio, fecha_fin)
        balance_data = json.loads(balance_json)

        # Configurar la tabla
        self.tabla_balance.setRowCount(len(balance_data))

        # Llenar la tabla con los datos
        for row, item in enumerate(balance_data):
            self.tabla_balance.setItem(row, 0, QTableWidgetItem(str(item['id_cuenta'])))
            self.tabla_balance.setItem(row, 1, QTableWidgetItem(item['nombre_cuenta']))
            self.tabla_balance.setItem(row, 2, QTableWidgetItem(f"{item['debe']:.2f}"))
            self.tabla_balance.setItem(row, 3, QTableWidgetItem(f"{item['haber']:.2f}"))

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

