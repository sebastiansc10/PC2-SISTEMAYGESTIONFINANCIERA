import sys
import json
import csv
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFileDialog, QHeaderView, QTableWidget, QLabel
)
from PyQt5.QtCore import QDate
from app.db_connection import obtener_conexion  # Conexión a PostgreSQL

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # ✅ Configuración de la Ventana Principal
        self.setWindowTitle("📊 Sistema Contable - Grupo 2")
        self.resize(1000, 750)
        self.showMaximized()  # 🔹 Maximiza la ventana al iniciar

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.layout.addWidget(self.stackedWidget)

        # ✅ Página Principal (Menú)
        self.page = QtWidgets.QWidget()
        self.page_layout = QVBoxLayout(self.page)

        self.label_2 = QLabel("📊 Sistema Contable - Grupo 2")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("font-size: 28px; font-weight: bold; color: #1E88E5; margin-bottom: 30px;")

        self.input = QPushButton("📜 Ver Diarios")
        self.output = QPushButton("📊 Ver Reportes")

        for btn in [self.input, self.output]:
            btn.setMinimumHeight(80)

        self.page_layout.addWidget(self.label_2)
        self.page_layout.addWidget(self.input)
        self.page_layout.addWidget(self.output)
        self.page.setLayout(self.page_layout)
        self.stackedWidget.addWidget(self.page)

        # ✅ Página de Diarios
        self.page_2 = QtWidgets.QWidget()
        self.page2_layout = QVBoxLayout(self.page_2)

        self.label = QLabel("📜 Diarios Registrados")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1565C0; margin-bottom: 10px;")

        # ✅ Barra de Búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Buscar en glosas...")
        self.search_bar.textChanged.connect(self.filtrar_tabla)

        # ✅ Tabla de Diarios
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "📝 Glosa", "📅 Fecha"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # ✅ Botones de Acción
        self.btn_add = QPushButton("➕ Agregar Fila")
        self.btn_delete = QPushButton("🗑️ Eliminar Fila")
        self.btn_export = QPushButton("📤 Exportar CSV")
        self.btn_save = QPushButton("💾 Guardar Cambios")

        self.btn_add.clicked.connect(self.agregar_fila)
        self.btn_delete.clicked.connect(self.eliminar_fila)
        self.btn_export.clicked.connect(self.exportar_csv)  # 🔹 Ahora está agregada correctamente
        self.btn_save.clicked.connect(self.guardar_cambios)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_export)

        self.page2_layout.addWidget(self.label)
        self.page2_layout.addWidget(self.search_bar)
        self.page2_layout.addWidget(self.tableWidget)
        self.page2_layout.addLayout(btn_layout)
        self.page_2.setLayout(self.page2_layout)
        self.stackedWidget.addWidget(self.page_2)

        self.input.clicked.connect(self.mostrar_diarios)

    def mostrar_diarios(self):
        """✅ Muestra la tabla de diarios con datos de PostgreSQL."""
        self.stackedWidget.setCurrentIndex(1)
        self.cargar_datos()

    def cargar_datos(self):
        """✅ Cargar datos desde PostgreSQL en la tabla."""
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_diario, glosa, fecha FROM diario ORDER BY fecha ASC")
            rows = cursor.fetchall()
            conn.close()

            self.tableWidget.setRowCount(len(rows))
            for row_idx, (id_diario, glosa, fecha) in enumerate(rows):
                self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(id_diario)))
                self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(glosa))

                fecha_str = fecha.strftime("%Y-%m-%d")  
                date_edit = QDateEdit()
                date_edit.setDate(QDate.fromString(fecha_str, "yyyy-MM-dd"))
                self.tableWidget.setCellWidget(row_idx, 2, date_edit)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos.\n{e}")

    def filtrar_tabla(self):
        """✅ Filtra la tabla en tiempo real según la barra de búsqueda."""
        filtro = self.search_bar.text().lower()
        for row in range(self.tableWidget.rowCount()):
            glosa = self.tableWidget.item(row, 1).text().lower()
            self.tableWidget.setRowHidden(row, filtro not in glosa)

    def agregar_fila(self):
        """✅ Agrega una nueva fila a la tabla."""
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        self.tableWidget.setItem(row_count, 0, QTableWidgetItem("Nuevo"))
        self.tableWidget.setItem(row_count, 1, QTableWidgetItem(""))
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        self.tableWidget.setCellWidget(row_count, 2, date_edit)

    def eliminar_fila(self):
        """✅ Elimina la fila seleccionada."""
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            id_diario = self.tableWidget.item(selected_row, 0).text()
            self.tableWidget.removeRow(selected_row)

            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM diario WHERE id_diario = %s", (id_diario,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Éxito", "Fila eliminada correctamente.")
        else:
            QMessageBox.warning(self, "Error", "Seleccione una fila para eliminar.")

    def guardar_cambios(self):
        """✅ Guarda los cambios en PostgreSQL."""
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            for row in range(self.tableWidget.rowCount()):
                id_diario = self.tableWidget.item(row, 0).text()
                glosa = self.tableWidget.item(row, 1).text()
                fecha_widget = self.tableWidget.cellWidget(row, 2)
                fecha = fecha_widget.date().toString("yyyy-MM-dd")

                cursor.execute(
                    "UPDATE diario SET glosa = %s, fecha = %s WHERE id_diario = %s",
                    (glosa, fecha, id_diario)
                )

            conn.commit()
            conn.close()
            QMessageBox.information(self, "Éxito", "Cambios guardados correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron guardar los cambios.\n{e}")

    def exportar_csv(self):
        """✅ Exporta la tabla a un archivo CSV."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar como", "", "Archivos CSV (*.csv)")
        if file_path:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Glosa", "Fecha"])
                for row in range(self.tableWidget.rowCount()):
                    writer.writerow([
                        self.tableWidget.item(row, 0).text(),
                        self.tableWidget.item(row, 1).text(),
                        self.tableWidget.cellWidget(row, 2).date().toString("yyyy-MM-dd")
                    ])
            QMessageBox.information(self, "Éxito", "CSV exportado correctamente.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_MainWindow()
    ventana.showMaximized()
    sys.exit(app.exec_())
