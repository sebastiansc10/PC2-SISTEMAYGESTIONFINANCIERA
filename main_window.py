import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFileDialog, QHeaderView, QTableWidget, QScrollArea
)
from PyQt5.QtCore import QDate
from app.funciones.DiarioTransaccion import mostrar_diario  # Asegúrate de que este módulo existe
import csv
from page1 import Page1
from page2 import Page2
from page3 import Page3

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Sistema Contable - Grupo 2")
        self.resize(1200, 800)
        self.setStyleSheet("""
            background-color: #f5f5f5;
            font-family: Arial;
            font-size: 14px;
        """)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.layout = QVBoxLayout(self.centralwidget)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.layout.addWidget(self.stackedWidget)

        # Inicializar páginas
        self.page1 = Page1()
        self.page2 = Page2()
        self.page3 = Page3()

        # Agregar páginas al stacked widget
        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)

        # Conectar botones
        self.page1.input.clicked.connect(self.mostrar_diarios)
        self.page1.output.clicked.connect(self.mostrar_formulario_reporte)

        self.fechainicio = None
        self.fechafin = None

    #def setup_main_page(self):
    #    #This function is no longer needed.
    #    pass

    #def setup_diarios_page(self):
    #    #This function is no longer needed.
    #    pass

    #def setup_reportes_page(self):
    #    #This function is no longer needed.
    #    pass


    def mostrar_diarios(self):
        """Muestra la página de diarios y llena la tabla."""
        self.stackedWidget.setCurrentIndex(1)
        datos = self.page2.obtener_diarios()
        self.page2.poblar_tabla(datos)

    def mostrar_formulario_reporte(self):
        """Muestra el formulario para ingresar las fechas de inicio y cierre."""
        self.formulario_reporte = QtWidgets.QWidget()
        formulario_layout = QVBoxLayout(self.formulario_reporte)

        self.fecha_inicio_label = QtWidgets.QLabel("Fecha de inicio:")
        self.fecha_inicio = QtWidgets.QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)

        self.fecha_cierre_label = QtWidgets.QLabel("Fecha de cierre:")
        self.fecha_cierre = QtWidgets.QDateEdit()
        self.fecha_cierre.setCalendarPopup(True)

        self.generar_reporte_btn = QtWidgets.QPushButton("Generar reporte")
        self.cerrar_ventana_btn = QtWidgets.QPushButton("Cerrar ventana")

        self.generar_reporte_btn.setStyleSheet("""
            background-color: #009688;
            color: white;
            padding: 8px;
            border-radius: 5px;
        """)
        self.cerrar_ventana_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 8px;
            border-radius: 5px;
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
        self.formulario_reporte.setWindowTitle("Seleccionar fechas de reporte")
        self.formulario_reporte.setGeometry(400, 300, 400, 250)
        self.formulario_reporte.show()

    def generar_reporte(self):
        """Guardar las fechas, actualizar el subtítulo y cambiar a la página 3."""
        self.fechainicio = self.fecha_inicio.date().toString("dd/MM/yyyy")
        self.fechafin = self.fecha_cierre.date().toString("dd/MM/yyyy")
    
        # Actualizar el subtítulo con las fechas
        self.page3.actualizar_fechas(self.fechainicio, self.fechafin)
    
        self.stackedWidget.setCurrentIndex(2)  # Cambia a la página de reportes
        self.formulario_reporte.close()  # Cierra el formulario

    def cerrar_ventana(self):
        """Cerrar la ventana del formulario."""
        self.formulario_reporte.close()

    #def obtener_diarios(self):
    #    #This function is no longer needed.
    #    pass

    #def poblar_tabla(self, datos):
    #    #This function is no longer needed.
    #    pass

    #def agregar_fila(self):
    #    #This function is no longer needed.
    #    pass

    #def eliminar_fila(self):
    #    #This function is no longer needed.
    #    pass

    #def filtrar_tabla(self):
    #    #This function is no longer needed.
    #    pass

    #def exportar_csv(self):
    #    #This function is no longer needed.
    #    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_MainWindow()
    ventana.show()
    sys.exit(app.exec_())

