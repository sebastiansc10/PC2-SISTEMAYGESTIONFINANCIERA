from PyQt5 import QtWidgets, QtCore, QtGui

STONE_GREEN = "#00B15D"   # verde tipo Stone
STONE_GREEN_HOVER = "#009A51"
STONE_ORANGE = "#FF8A00"
STONE_ORANGE_HOVER = "#E67600"
TEXT_DARK = "#243447"

class Page1(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Fondo suave (sin panel negro)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0,y1:0, x2:1,y2:1,
                    stop:0 #F7FAFC, stop:1 #ECF3F7);
                color: %s;
                font-family: 'Segoe UI', Arial;
            }
        """ % TEXT_DARK)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 24)
        root.setSpacing(16)

        # Tarjeta central (blanca, bordes redondeados + sombra)
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E6ECF1;
            }
        """)
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        # Sombra
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 8)
        shadow.setColor(QtGui.QColor(0, 0, 0, 35))
        card.setGraphicsEffect(shadow)

        # Título
        self.title = QtWidgets.QLabel("Sistema Contable - Grupo 7")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 22px; font-weight: 800;
                letter-spacing: 0.3px;
            }
        """)

        # Imagen/logo (ajuste dentro de card)
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setMinimumHeight(320)
        pix = QtGui.QPixmap("assets/contabilidad2.png")
        if pix.isNull():
            pix = QtGui.QPixmap("assets/logo.png")
        self.image_label.setPixmap(pix.scaled(540, 320, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.image_label.setStyleSheet("border-radius:12px;")

        # Botones estilo StoneCo
        self.btn_diarios = self._stone_button("Ver Diarios", primary=True)
        self.btn_reportes = self._stone_button("Ver Reportes", primary=False)

        btns = QtWidgets.QHBoxLayout()
        btns.setSpacing(14)
        btns.addStretch(1)
        btns.addWidget(self.btn_diarios, 0)
        btns.addWidget(self.btn_reportes, 0)
        btns.addStretch(1)

        # Armar card
        card_layout.addWidget(self.title)
        card_layout.addSpacing(6)
        card_layout.addWidget(self.image_label, 1)
        card_layout.addSpacing(8)
        card_layout.addLayout(btns)

        # Centrar card en la página
        wrapper = QtWidgets.QHBoxLayout()
        wrapper.addStretch(1)
        wrapper.addWidget(card, 0)
        wrapper.addStretch(1)

        root.addStretch(1)
        root.addLayout(wrapper)
        root.addStretch(1)

    def _stone_button(self, text, primary=True):
        btn = QtWidgets.QPushButton(text)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setMinimumHeight(50)
        btn.setMinimumWidth(180)
        btn.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        if primary:
            base = STONE_GREEN
            hover = STONE_GREEN_HOVER
        else:
            base = STONE_ORANGE
            hover = STONE_ORANGE_HOVER

        btn.setStyleSheet(f"""
            QPushButton {{
                background: {base};
                color: #FFFFFF;
                font-size: 16px; font-weight: 700;
                padding: 12px 18px;
                border: none;
                border-radius: 10px;
                box-shadow: 0px 6px 14px rgba(0,0,0,0.12);
            }}
            QPushButton:hover {{ background: {hover}; }}
            QPushButton:pressed {{
                transform: translateY(1px);
                background: {hover};
                box-shadow: 0px 3px 10px rgba(0,0,0,0.16);
            }}
            QPushButton:focus {{ outline: none; }}
        """)
        return btn
