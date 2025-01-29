import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFileDialog, QHeaderView, QTableWidget
)
from PyQt5.QtCore import QDate
from app.funciones.DiarioTransaccion import mostrar_diario  # Asegúrate de que este módulo existe

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

        # ✅ Página Principal
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

        # ✅ Página de Diarios
        self.page_2 = QtWidgets.QWidget()
        self.page2_layout = QVBoxLayout(self.page_2)

        self.label = QtWidgets.QLabel("📜 Diarios Registrados")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        # Barra de Búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Buscar en glosas...")
        self.search_bar.setStyleSheet("""
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        """)
        self.search_bar.textChanged.connect(self.filtrar_tabla)  # ✅ Corrección aquí

        # ✅ **Tabla Mejorada**
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["📝 Glosa", "📅 Fecha"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setAlternatingRowColors(True)  # ✅ Alternar colores de filas
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

        # ✅ Botones de Acción
        self.btn_add = QPushButton("➕ Agregar Fila")
        self.btn_delete = QPushButton("🗑️ Eliminar Fila")
        self.btn_export = QPushButton("📤 Exportar CSV")

        self.btn_add.setStyleSheet("background-color: #009688; color: white; padding: 8px; border-radius: 5px;")
        self.btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; border-radius: 5px;")
        self.btn_export.setStyleSheet("background-color: #f39c12; color: white; padding: 8px; border-radius: 5px;")

        self.btn_add.clicked.connect(self.agregar_fila)
        self.btn_delete.clicked.connect(self.eliminar_fila)
        self.btn_export.clicked.connect(self.exportar_csv)  # ✅ Corrección aquí

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

        # ✅ Conectar botones
        self.input.clicked.connect(self.mostrar_diarios)

    def mostrar_diarios(self):
        """Muestra la página de diarios y llena la tabla."""
        self.stackedWidget.setCurrentIndex(1)
        datos = self.obtener_diarios()
        self.poblar_tabla(datos)

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
