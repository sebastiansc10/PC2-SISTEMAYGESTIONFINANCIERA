from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout

class Page1(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.page_layout = QVBoxLayout(self)

        self.label_2 = QtWidgets.QLabel("📊 Sistema Contable - Grupo 2")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")

        self.input = QPushButton("📜 Ver diarios")
        self.input.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        """)
        self.output = QPushButton("📊 Ver reportes")
        self.output.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        """)

        self.page_layout.addWidget(self.label_2)
        self.page_layout.addWidget(self.input)
        self.page_layout.addWidget(self.output)
        self.setLayout(self.page_layout)

