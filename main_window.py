import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from page1 import Page1
from page2 import Page2
from page3 import Page3
from datetime import datetime

# ── Paleta StoneCo + helper de botón ─────────────────────────────────────────
STONE = {
    "bg":          "#0f1412",   # fondo app
    "card":        "#151a18",   # tarjetas / paneles
    "text":        "#ffffff",
    "muted":       "#cfe7d8",

    # Verdes corporativos
    "g1":          "#00A859",   # primary
    "g2":          "#00C853",   # light
    "g_dark":      "#008C4A",   # hover/pressed
    "g_outline":   "#1a3c2d",   # bordes sutiles

    # Acentos / estados
    "accent":      "#1DE9B6",
    "danger":      "#e74c3c",
    "gray":        "#95a5a6",
    "gray_dark":   "#7f8c8d"
}

def stone_button(btn: QtWidgets.QPushButton, kind: str = "primary"):
    """kind: primary | secondary | danger"""
    if kind == "secondary":
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {STONE['gray_dark']};
                color: {STONE['text']};
                padding: 12px 18px;
                border-radius: 10px;
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
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {STONE['danger']};
                color: {STONE['text']};
                padding: 12px 18px;
                border-radius: 10px;
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
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                         stop:0 {STONE['g1']}, stop:1 {STONE['g2']});
                color: {STONE['text']};
                padding: 12px 18px;
                border-radius: 10px;
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
    f = btn.font()
    f.setPointSize(16)
    f.setBold(True)
    btn.setFont(f)
    btn.setCursor(QtCore.Qt.PointingHandCursor)
    btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    btn.setMinimumHeight(50)

def stone_dateedit():
    de = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
    de.setCalendarPopup(True)
    de.setDisplayFormat("dd/MM/yyyy")

    # Input blanco / texto negro
    de.setStyleSheet("""
        QDateEdit {
            background-color: #ffffff;
            color: #111111;
            border: 1px solid #D1D5DB;
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 16px;
            min-height: 38px;
        }
        QDateEdit:hover { border: 1px solid #9CA3AF; }
        QDateEdit:focus  { border: 2px solid #1DE9B6; background: #ffffff; }
        QDateEdit::drop-down {
            width: 24px;
            subcontrol-origin: padding; subcontrol-position: right center;
        }
    """)

    cal = de.calendarWidget()

    # Comportamiento base
    cal.setGridVisible(True)
    cal.setFirstDayOfWeek(QtCore.Qt.Monday)
    cal.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
    cal.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
    cal.setNavigationBarVisible(True)
    cal.setMinimumWidth(340)  
    # Botones del header (plano, sin borde)
    prev_btn  = cal.findChild(QtWidgets.QToolButton, "qt_calendar_prevmonth")
    next_btn  = cal.findChild(QtWidgets.QToolButton, "qt_calendar_nextmonth")
    month_btn = cal.findChild(QtWidgets.QToolButton, "qt_calendar_monthbutton")
    year_btn  = cal.findChild(QtWidgets.QToolButton, "qt_calendar_yearbutton")
    for b in (prev_btn, next_btn, month_btn, year_btn):
        if b:
            b.setIcon(QtGui.QIcon())
            b.setCursor(QtCore.Qt.PointingHandCursor)
            b.setMinimumHeight(28)
    if prev_btn: prev_btn.setText("◄"); prev_btn.setToolTip("Mes anterior")
    if next_btn: next_btn.setText("►"); next_btn.setToolTip("Mes siguiente")

    # Quitar fines de semana rojos → todo negro
    fmt_clear = QtGui.QTextCharFormat()
    cal.setWeekdayTextFormat(QtCore.Qt.Saturday, fmt_clear)
    cal.setWeekdayTextFormat(QtCore.Qt.Sunday,   fmt_clear)

    # "Hoy" con texto negro
    fmt_today = QtGui.QTextCharFormat()
    fmt_today.setForeground(QtGui.QBrush(QtGui.QColor("#111111")))
    cal.setDateTextFormat(QtCore.QDate.currentDate(), fmt_today)

    # Estilos: header plano y celdas sin márgenes (para que entren los 7 días)
    cal.setStyleSheet("""
        /* Contenedor */
        QCalendarWidget {
            background-color: #ffffff;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
        }

        /* Barra de navegación (encabezado) */
        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background: #ffffff;
            border: none;                       /* <-- sin bordes */
            min-height: 34px;
            padding: 4px 6px;
        }

        /* Botones del header (mes, año, flechas) */
        QCalendarWidget QToolButton {
            background: transparent;
            color: #111111;
            font-weight: 700;
            padding: 2px 6px;
            border: none;                       /* <-- sin borde */
            border-radius: 6px;
            min-width: 24px;
        }
        QCalendarWidget QToolButton:hover {
            background-color: #F3F4F6;
        }
        /* Sin triángulo de menú en el mes */
        QCalendarWidget QToolButton::menu-indicator { image: none; }

        /* Cabecera de días (Lu, Ma, ...) */
        QCalendarWidget QTableView QHeaderView::section {
            background-color: #ffffff;
            color: #6B7280;
            border: none;
            padding: 4px 0;
            font-weight: 700;
        }

        /* Tabla de días */
        QCalendarWidget QTableView {
            outline: 0;
            gridline-color: #E5E7EB;
            background: #ffffff;
            margin: 0px;                        /* <-- sin márgenes */
        }
        QCalendarWidget QAbstractItemView:enabled {
            background: #ffffff;
            color: #111111;
        }
        QCalendarWidget QAbstractItemView:disabled {
            color: #9CA3AF;
        }

        /* Ítems: padding mínimo para no cortar columnas */
        QCalendarWidget QAbstractItemView::item {
            margin: 0px;
            padding: 0px;                       
            border-radius: 8px;
        }
        QCalendarWidget QAbstractItemView::item:hover {
            background-color: #F3F4F6;
        }
        QCalendarWidget QAbstractItemView::item:selected {
            background-color: #E8F5E9;
            color: #111111;
            border: 2px solid #00C853;
        }
    """)

    # (Opcional) Ensancha un poquito por si el estilo del sistema es muy “gordo”
    view = cal.findChild(QtWidgets.QTableView, "qt_calendar_calendarview")
    if view:
        view.setContentsMargins(0, 0, 0, 0)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    return de


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Contable - Grupo 7")
        self.resize(1200, 800)
        # Mantengo tu estilo general claro; el popup de fechas irá en StoneCo
        self.setStyleSheet("""
            background-color: #F2F2F2;
            color: #2C3E50;
            font-family: 'Segoe UI', Arial;
        """)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.layout.addWidget(self.stackedWidget)

        self.page1 = Page1(self)
        self.page2 = Page2(self)
        self.page3 = Page3(self)

        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)

        self.page1.btn_diarios.clicked.connect(self.mostrar_diarios)
        self.page1.btn_reportes.clicked.connect(self.mostrar_formulario_reporte)

        self.showMaximized()

    def mostrar_diarios(self):
        self.stackedWidget.setCurrentIndex(1)
        datos = self.page2.obtener_diarios()
        self.page2.poblar_tabla(datos)

    def mostrar_formulario_reporte(self):
        """Popup de fechas con tema StoneCo (mismo popup que Page2)."""
        self.formulario_reporte = QtWidgets.QWidget()
        self.formulario_reporte.setWindowTitle("Seleccionar Fechas para el Reporte")

        # Centrar ventana
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        width, height = 420, 280
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        self.formulario_reporte.setGeometry(x, y, width, height)

        formulario_layout = QtWidgets.QVBoxLayout(self.formulario_reporte)

        # Contenedor estilo "card" StoneCo
        self.formulario_reporte.setStyleSheet(f"""
            QWidget {{
                background-color: {STONE['card']};
                color: {STONE['text']};
                border: 1px solid {STONE['g_outline']};
                border-radius: 12px;
                padding: 12px;
            }}
            QLabel {{
                color: {STONE['muted']};
                font-size: 14px;
                font-weight: 700;
            }}
        """)

        # Título
        self.label_titulo = QtWidgets.QLabel("Seleccionar Fechas para el Reporte")
        self.label_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo.setStyleSheet(f"""
            font-size: 18px; font-weight: 800; color: {STONE['g2']};
            margin-bottom: 12px;
        """)

        self.fecha_inicio_label = QtWidgets.QLabel("Fecha de inicio:")
        self.fecha_cierre_label = QtWidgets.QLabel("Fecha de cierre:")

        # DateEdits (usan el helper con el mismo popup que Page2)
        self.fecha_inicio = stone_dateedit()
        self.fecha_cierre = stone_dateedit()

        # Botones StoneCo
        self.generar_reporte_btn = QtWidgets.QPushButton("Generar reporte")
        self.cerrar_ventana_btn = QtWidgets.QPushButton("Cerrar ventana")
        stone_button(self.generar_reporte_btn, "primary")
        stone_button(self.cerrar_ventana_btn, "danger")

        # Conectar
        self.generar_reporte_btn.clicked.connect(self.generar_reporte)
        self.cerrar_ventana_btn.clicked.connect(self.cerrar_ventana)

        # Layout
        formulario_layout.addWidget(self.label_titulo)
        formulario_layout.addWidget(self.fecha_inicio_label)
        formulario_layout.addWidget(self.fecha_inicio)
        formulario_layout.addWidget(self.fecha_cierre_label)
        formulario_layout.addWidget(self.fecha_cierre)

        botones = QtWidgets.QHBoxLayout()
        botones.addWidget(self.generar_reporte_btn)
        botones.addWidget(self.cerrar_ventana_btn)
        formulario_layout.addLayout(botones)

        self.formulario_reporte.setLayout(formulario_layout)
        self.formulario_reporte.show()

    def generar_reporte(self):
        fechainicio = self.fecha_inicio.date().toString("dd/MM/yyyy")
        fechafin = self.fecha_cierre.date().toString("dd/MM/yyyy")

        fechainicio_pg = datetime.strptime(fechainicio, "%d/%m/%Y").strftime("%Y-%m-%d")
        fechafin_pg    = datetime.strptime(fechafin,    "%d/%m/%Y").strftime("%Y-%m-%d")

        self.page3.actualizar_fechas(fechainicio_pg, fechafin_pg)
        self.stackedWidget.setCurrentIndex(2)
        self.formulario_reporte.close()

    def cerrar_ventana(self):
        self.formulario_reporte.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_MainWindow()
    ventana.show()
    sys.exit(app.exec_())
