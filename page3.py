from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QDateEdit, QPushButton

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

            # Agregar contenido de ejemplo para cada sección
            for i in range(5):  # 5 registros de ejemplo por sección
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

