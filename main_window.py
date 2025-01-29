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
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fa, stop:1 #e9ecef);
        """)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.layout.addWidget(self.stackedWidget)

        # Inicializar páginas
        self.page1 = Page1(self)
        self.page2 = Page2(self)
        self.page3 = Page3(self)

        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)

        # Conectar botones de navegación
        self.page1.btn_diarios.clicked.connect(self.mostrar_diarios)
        self.page1.btn_reportes.clicked.connect(self.mostrar_formulario_reporte)

        self.showMaximized()

    def mostrar_diarios(self):
        """Muestra la página de diarios."""
        self.stackedWidget.setCurrentIndex(1)
        datos = self.page2.obtener_diarios()
        self.page2.poblar_tabla(datos)

    def mostrar_formulario_reporte(self):
        """Muestra el formulario para ingresar las fechas antes de ver reportes."""
        self.formulario_reporte = QtWidgets.QWidget()
        formulario_layout = QtWidgets.QVBoxLayout(self.formulario_reporte)

        self.fecha_inicio_label = QtWidgets.QLabel("📅 Fecha de inicio:")
        self.fecha_inicio = QtWidgets.QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QtCore.QDate.currentDate())

        self.fecha_cierre_label = QtWidgets.QLabel("📅 Fecha de cierre:")
        self.fecha_cierre = QtWidgets.QDateEdit()
        self.fecha_cierre.setCalendarPopup(True)
        self.fecha_cierre.setDate(QtCore.QDate.currentDate())

        self.generar_reporte_btn = QtWidgets.QPushButton("📊 Generar Reporte")
        self.cerrar_ventana_btn = QtWidgets.QPushButton("❌ Cerrar Ventana")

        # Estilos de botones
        self.generar_reporte_btn.setStyleSheet("""
            background-color: #009688;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        """)
        self.cerrar_ventana_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        """)

        self.generar_reporte_btn.clicked.connect(self.generar_reporte)
        self.cerrar_ventana_btn.clicked.connect(self.cerrar_ventana)

        formulario_layout.addWidget(self.fecha_inicio_label)
        formulario_layout.addWidget(self.fecha_inicio)
        formulario_layout.addWidget(self.fecha_cierre_label)
        formulario_layout.addWidget(self.fecha_cierre)
        formulario_layout.addWidget(self.generar_reporte_btn)
        formulario_layout.addWidget(self.cerrar_ventana_btn)

        self.formulario_reporte.setLayout(formulario_layout)
        self.formulario_reporte.setWindowTitle("Seleccionar Fechas para el Reporte")
        self.formulario_reporte.setGeometry(500, 300, 400, 250)
        self.formulario_reporte.show()

    def generar_reporte(self):
        """Guarda las fechas seleccionadas y muestra la página de reportes."""
        fechainicio = self.fecha_inicio.date().toString("dd/MM/yyyy")
        fechafin = self.fecha_cierre.date().toString("dd/MM/yyyy")

        # Enviar fechas a Page3 para actualizar los datos
        self.page3.actualizar_fechas(fechainicio, fechafin)

        self.stackedWidget.setCurrentIndex(2)  # Ir a la página de reportes
        self.formulario_reporte.close()  # Cerrar el formulario

    def cerrar_ventana(self):
        """Cerrar la ventana del formulario de fechas."""
        self.formulario_reporte.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_MainWindow()
    ventana.show()
    sys.exit(app.exec_())
