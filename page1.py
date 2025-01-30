from PyQt5 import QtWidgets, QtGui, QtCore

class Page1(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #000000, stop:1 #1a1a1a);
                color: white;
            }
        """)

        self.title = QtWidgets.QLabel("💼 Sistema Contable - Grupo 2")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #f1c40f;
        """)
        self.layout.addWidget(self.title)

        self.image_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("assets/contabilidad2.png")
        self.image_label.setPixmap(pixmap.scaled(650, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border-radius: 10px;
                border: 3px solid #666;
                padding: 5px;
                background-color: #222;
            }
        """)
        self.layout.addWidget(self.image_label)

        self.button_container = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.btn_diarios = QtWidgets.QPushButton("📜 Ver Diarios")
        self.btn_diarios.setStyleSheet(self.button_style("#1DB954", "#1AAE45"))
        self.btn_diarios.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_layout.addWidget(self.btn_diarios)

        self.btn_reportes = QtWidgets.QPushButton("📈 Ver Reportes")
        self.btn_reportes.setStyleSheet(self.button_style("#FF9800", "#FB8C00"))
        self.btn_reportes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_layout.addWidget(self.btn_reportes)

        self.layout.addWidget(self.button_container)

    def button_style(self, color, hover_color):
        return f"""
        QPushButton {{
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {color}, stop:1 {hover_color});
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #444;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: #000000;
        }}
        """
