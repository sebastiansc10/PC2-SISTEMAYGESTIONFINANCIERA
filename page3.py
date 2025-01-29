from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QDateEdit, QPushButton

class Page3(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.page3_layout = QVBoxLayout(self)

        # Título principal
        self.titulo_principal = QtWidgets.QLabel("Estado de situación financiera")
        self.titulo_principal.setAlignment(QtCore.Qt.AlignCenter)
        self.titulo_principal.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #2C3E50;
    """)

        # Subtítulo con fechas
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

        for i in range(30):  # Ejemplo de contenido
            label = QtWidgets.QLabel(f"Registro contable {i + 1}")
            label.setStyleSheet("font-size: 16px; padding: 10px;")
            content_layout.addWidget(label)

        self.scroll_area.setWidget(content_widget)

        self.page3_layout.addWidget(self.titulo_principal)
        self.page3_layout.addWidget(self.subtitulo_fechas)
        self.page3_layout.addWidget(self.scroll_area)
        self.setLayout(self.page3_layout)

    def actualizar_fechas(self, fecha_inicio, fecha_fin):
        self.subtitulo_fechas.setText(f"Desde {fecha_inicio} hasta {fecha_fin}")

