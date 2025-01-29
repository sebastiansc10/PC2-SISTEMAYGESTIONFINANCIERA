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

        # Página Principal
        self.setup_main_page()

        # Página de Diarios
        self.setup_diarios_page()

        # Página de Reportes
        self.setup_reportes_page()

        # Conectar botones
        self.input.clicked.connect(self.mostrar_diarios)
        self.output.clicked.connect(self.mostrar_formulario_reporte)

        self.fechainicio = None
        self.fechafin = None

    def setup_main_page(self):
        self.page = QtWidgets.QWidget()
        self.page_layout = QVBoxLayout(self.page)

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
        self.page.setLayout(self.page_layout)
        self.stackedWidget.addWidget(self.page)

    def setup_diarios_page(self):
        self.page_2 = QtWidgets.QWidget()
        self.page2_layout = QVBoxLayout(self.page_2)

        self.label = QtWidgets.QLabel("📜 Diarios Registrados")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Buscar en glosas...")
        self.search_bar.setStyleSheet("""
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        """)
        self.search_bar.textChanged.connect(self.filtrar_tabla)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["📝 Glosa", "📅 Fecha"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 5px;
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #ccc;
            }
            QTableWidget::item:selected {
                background-color: #90CAF9;
                color: black;
            }
        """)

        self.btn_add = QPushButton("➕ Agregar Fila")
        self.btn_delete = QPushButton("🗑️ Eliminar Fila")
        self.btn_export = QPushButton("📤 Exportar CSV")

        self.btn_add.setStyleSheet("background-color: #009688; color: white; padding: 8px; border-radius: 5px;")
        self.btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; border-radius: 5px;")
        self.btn_export.setStyleSheet("background-color: #f39c12; color: white; padding: 8px; border-radius: 5px;")

        self.btn_add.clicked.connect(self.agregar_fila)
        self.btn_delete.clicked.connect(self.eliminar_fila)
        self.btn_export.clicked.connect(self.exportar_csv)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_export)

        self.page2_layout.addWidget(self.label)
        self.page2_layout.addWidget(self.search_bar)
        self.page2_layout.addWidget(self.tableWidget)
        self.page2_layout.addLayout(btn_layout)
        self.page_2.setLayout(self.page2_layout)
        self.stackedWidget.addWidget(self.page_2)

    def setup_reportes_page(self):
        self.page_3 = QtWidgets.QWidget()
        self.page3_layout = QVBoxLayout(self.page_3)

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
        self.page_3.setLayout(self.page3_layout)
        self.stackedWidget.addWidget(self.page_3)

    def mostrar_diarios(self):
        """Muestra la página de diarios y llena la tabla."""
        self.stackedWidget.setCurrentIndex(1)
        datos = self.obtener_diarios()
        self.poblar_tabla(datos)

    def mostrar_formulario_reporte(self):
        """Muestra el formulario para ingresar las fechas de inicio y cierre."""
        self.formulario_reporte = QtWidgets.QWidget()
        formulario_layout = QVBoxLayout(self.formulario_reporte)

        self.fecha_inicio_label = QtWidgets.QLabel("Fecha de inicio:")
        self.fecha_inicio = QDateEdit(QDate.currentDate())
        self.fecha_inicio.setCalendarPopup(True)

        self.fecha_cierre_label = QtWidgets.QLabel("Fecha de cierre:")
        self.fecha_cierre = QDateEdit(QDate.currentDate())
        self.fecha_cierre.setCalendarPopup(True)

        self.generar_reporte_btn = QPushButton("Generar reporte")
        self.cerrar_ventana_btn = QPushButton("Cerrar ventana")

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
        self.subtitulo_fechas.setText(f"Desde {self.fechainicio} hasta {self.fechafin}")
    
        self.stackedWidget.setCurrentIndex(2)  # Cambia a la página de reportes
        self.formulario_reporte.close()  # Cierra el formulario

    def cerrar_ventana(self):
        """Cerrar la ventana del formulario."""
        self.formulario_reporte.close()

    def obtener_diarios(self):
        """Obtiene los datos de la base de datos."""
        resultado_json = mostrar_diario()
        resultado = json.loads(resultado_json)
        return [(glosa, fecha) for fecha, glosa in resultado.items()]

    def poblar_tabla(self, datos):
        """Llena la tabla y agrega QDateEdit en la columna Fecha."""
        self.tableWidget.setRowCount(len(datos))
        for row, (glosa, fecha) in enumerate(datos):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(glosa))

            date_widget = QDateEdit()
            date_widget.setCalendarPopup(True)
            date_widget.setDate(QDate.fromString(fecha, "yyyy-MM-dd"))
            self.tableWidget.setCellWidget(row, 1, date_widget)

    def agregar_fila(self):
        """Agrega una nueva fila con un QDateEdit en la columna de fecha."""
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem("Nueva Glosa"))

        date_widget = QDateEdit()
        date_widget.setCalendarPopup(True)
        date_widget.setDate(QDate.currentDate())
        self.tableWidget.setCellWidget(row, 1, date_widget)

    def eliminar_fila(self):
        """Elimina la fila seleccionada."""
        row = self.tableWidget.currentRow()
        if row >= 0:
            self.tableWidget.removeRow(row)
        else:
            QMessageBox.warning(self, "Error", "Seleccione una fila para eliminar.")

    def filtrar_tabla(self):
        """Filtra la tabla en base al texto ingresado en la barra de búsqueda."""
        filtro = self.search_bar.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            if item and filtro in item.text().lower():
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)

    def exportar_csv(self):
        """Exporta los datos de la tabla a un archivo CSV."""
        path, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", "", "Archivos CSV (*.csv)")
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write("Glosa,Fecha\n")
                for row in range(self.tableWidget.rowCount()):
                    glosa = self.tableWidget.item(row, 0).text()
                    fecha = self.tableWidget.cellWidget(row, 1).date().toString("yyyy-MM-dd")
                    file.write(f"{glosa},{fecha}\n")
            QMessageBox.information(self, "Éxito", "El archivo CSV ha sido guardado correctamente.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_MainWindow()
    ventana.show()
    sys.exit(app.exec_())

