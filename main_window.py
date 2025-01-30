import sys
from PyQt5 import QtWidgets, QtCore
from page1 import Page1
from page2 import Page2
from page3 import Page3

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Sistema Contable - Grupo 2")
        self.resize(1200, 800)
        self.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #000000, stop:1 #1a1a1a);
            color: #ffffff;
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
        """ Muestra el formulario para seleccionar las fechas del reporte con un diseño mejorado y centrado. """
        
        self.formulario_reporte = QtWidgets.QWidget()
        self.formulario_reporte.setWindowTitle("📅 Seleccionar Fechas para el Reporte")
        
        # 🔹 Centrar la ventana en la pantalla
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        width, height = 400, 300  # Tamaño fijo de la ventana
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        self.formulario_reporte.setGeometry(x, y, width, height)
        
        formulario_layout = QtWidgets.QVBoxLayout(self.formulario_reporte)

        # 🔹 Título del formulario
        self.label_titulo = QtWidgets.QLabel("📅 Seleccionar Fechas para el Reporte")
        self.label_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 15px;")

        # 🔹 Fecha de Inicio
        self.fecha_inicio_label = QtWidgets.QLabel("📅 Fecha de inicio:")
        self.fecha_inicio_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.fecha_inicio = QtWidgets.QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QtCore.QDate.currentDate())

        # 🔹 Fecha de Cierre
        self.fecha_cierre_label = QtWidgets.QLabel("📅 Fecha de cierre:")
        self.fecha_cierre_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.fecha_cierre = QtWidgets.QDateEdit()
        self.fecha_cierre.setCalendarPopup(True)
        self.fecha_cierre.setDate(QtCore.QDate.currentDate())

        # 🔹 Aplicar el mismo estilo a ambos `QDateEdit`
        date_edit_style = """
            QDateEdit {
                background-color: #1a1a1a;
                color: white;
                font-size: 16px;
                border: 1px solid #444;
                padding: 6px;
                border-radius: 6px;
            }
            QDateEdit:hover {
                background-color: #2a2a2a;
                border: 1px solid #0078D7;
            }
            QDateEdit:focus {
                background-color: #2a2a2a;
                border: 1px solid #444; /* 🔹 Se eliminan los bordes azules al enfocar */
            }
            QCalendarWidget QWidget {
                background-color: #1a1a1a;
                color: white;
                border: none;
            }
            QCalendarWidget QTableView {
                border: none;
            }
        """
        
        self.fecha_inicio.setStyleSheet(date_edit_style)
        self.fecha_cierre.setStyleSheet(date_edit_style)

        # 🔹 Botones mejorados
        self.generar_reporte_btn = self.create_button("📊 Generar Reporte", "#0078D7", "#005A9E")
        self.cerrar_ventana_btn = self.create_button("❌ Cerrar Ventana", "#e74c3c", "#c0392b")

        self.generar_reporte_btn.clicked.connect(self.generar_reporte)
        self.cerrar_ventana_btn.clicked.connect(self.cerrar_ventana)

        # 🔹 Añadir widgets al layout
        formulario_layout.addWidget(self.label_titulo)
        formulario_layout.addWidget(self.fecha_inicio_label)
        formulario_layout.addWidget(self.fecha_inicio)
        formulario_layout.addWidget(self.fecha_cierre_label)
        formulario_layout.addWidget(self.fecha_cierre)
        formulario_layout.addWidget(self.generar_reporte_btn)
        formulario_layout.addWidget(self.cerrar_ventana_btn)

        # 🔹 Aplicar el layout y mostrar la ventana
        self.formulario_reporte.setLayout(formulario_layout)
        self.formulario_reporte.setStyleSheet("border-radius: 12px; background-color: #222; padding: 15px;")
        self.formulario_reporte.show()

    def create_button(self, text, color, hover_color):
        """🔹 Genera botones con estilo profesional"""
        button = QtWidgets.QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {color}, stop:1 {color});
                color: white;
                padding: 14px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #444;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 2px solid white;
            }}
            QPushButton:pressed {{
                background-color: #00000044;
                border: 2px solid #fff;
            }}
        """)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        button.setMinimumHeight(50)
        return button

    def generar_reporte(self):
        fechainicio = self.fecha_inicio.date().toString("dd/MM/yyyy")
        fechafin = self.fecha_cierre.date().toString("dd/MM/yyyy")

        self.page3.actualizar_fechas(fechainicio, fechafin)
        self.stackedWidget.setCurrentIndex(2)
        self.formulario_reporte.close()

    def cerrar_ventana(self):
        self.formulario_reporte.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_MainWindow()
    ventana.show()
    sys.exit(app.exec_())