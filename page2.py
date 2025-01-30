import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFileDialog, QHeaderView, QTableWidget
)
from PyQt5.QtCore import QDate
from app.funciones.DiarioTransaccion import eliminar_diario, mostrar_diario, registrar_diario, actualizar_diario
from page4 import Page4

class CustomTableItem(QTableWidgetItem):
    def __init__(self, text):
        super().__init__(text)
        self.original_text = "(Nuevo)"
        
    def setText(self, text):
        # Ensure "(Nuevo)" prefix is always present
        if not text.startswith("(Nuevo)"):
            text = "(Nuevo)" + text
        super().setText(text)

class Page2(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.page2_layout = QVBoxLayout(self)

        self.label = QtWidgets.QLabel("📜 Diarios Registrados")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 22px; font-weight: bold; color: #f1c40f; margin-bottom: 10px;")



        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Buscar en glosas...")
        self.search_bar.setStyleSheet("""
            padding: 12px;  /* 🔹 Aumenta el espacio interno */
            border-radius: 8px;
            border: 1px solid #444;
            background-color: #222;
            color: white;
            font-size: 16px;  /* 🔹 Unifica el tamaño con la tabla */
            font-weight: bold;  /* 🔹 Negrita */
        """)

        self.search_bar.textChanged.connect(self.filtrar_tabla)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)  # 🔹 Oculta los índices de fila
        self.tableWidget.setHorizontalHeaderLabels(["📝 Glosa", "📅 Fecha"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #121212;
                gridline-color: #444;
                color: white;
                font-size: 16px;  /* 🔹 Unifica el tamaño con la barra de búsqueda */
                font-weight: bold;  /* 🔹 Negrita para mejorar visibilidad */
            }
            QTableWidget::item {
                background-color: #1a1a1a;
                color: white;
            }
            QHeaderView::section {
                background-color: #0078D7;
                color: white;
                padding: 8px;  /* 🔹 Aumenta el padding para mejor legibilidad */
                font-size: 16px;  /* 🔹 Hace las cabeceras más grandes */
                font-weight: bold;
                border: 1px solid #444;
            }
            QTableWidget::item:selected {
                background-color: #005A9E;
                color: white;
            }
        """)

        self.btn_add = self.create_button("➕ Agregar Fila", "#009688", "#00796B")  # 🔹 Verde oscuro
        self.btn_delete = self.create_button("🗑️ Eliminar Fila", "#e74c3c", "#c0392b")  # 🔹 Rojo oscuro
        self.btn_export = self.create_button("📤 Exportar CSV", "#f39c12", "#d68910")  # 🔹 Naranja oscuro
        self.btn_view_transaction = self.create_button("👁️ Ver Transacción", "#3498db", "#2980b9")  # 🔹 Azul oscuro
        self.btn_update = self.create_button("🔄 Actualizar Diarios", "#2ecc71", "#27ae60")  # 🔹 Verde claro
        self.btn_back = self.create_button("🏠 Volver al Inicio", "#95a5a6", "#7f8c8d")  # 🔹 Gris oscuro

        self.btn_add.clicked.connect(self.agregar_fila)
        self.btn_delete.clicked.connect(self.eliminar_fila)
        self.btn_export.clicked.connect(self.exportar_csv)
        self.btn_view_transaction.clicked.connect(self.ver_transaccion)
        self.btn_update.clicked.connect(self.actualizar_diarios)
        self.btn_back.clicked.connect(self.volver_al_inicio)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_view_transaction)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_back)

        self.page2_layout.addWidget(self.label)
        self.page2_layout.addWidget(self.search_bar)
        self.page2_layout.addWidget(self.tableWidget)
        self.page2_layout.addLayout(btn_layout)
        self.setLayout(self.page2_layout)

        self.actualizar_tabla()

    def create_button(self, text, color, hover_color):
        button = QPushButton(text)
        
        # 🔹 Asegura que el texto sea grande usando `setFont()`
        font = button.font()
        font.setPointSize(16)  # 🔹 Tamaño del texto
        font.setBold(True)  # 🔹 Negrita
        button.setFont(font)

        # 🔹 Aplica estilos en `setStyleSheet()`
        button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {color}, stop:1 {color});
                color: white;
                padding: 18px 30px;
                border-radius: 12px;
                font-size: 16px;  /* 🔹 También aseguramos el tamaño desde CSS */
                font-weight: bold;
                text-align: center;
                border: 2px solid #444;
            }}
            QPushButton:hover {{
                background-color: {hover_color};  /* 🔹 Color distinto al pasar el mouse */
                border: 2px solid white;
            }}
            QPushButton:pressed {{
                background-color: #00000044;
                border: 2px solid #fff;
            }}
        """)

        # 🔹 Asegura que el botón se expanda correctamente
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        button.setMinimumHeight(60)  # 🔹 Ajusta altura mínima
        button.setFixedHeight(60)  # 🔹 Forzar la altura

        return button

    def obtener_diarios(self):
        resultado_json = mostrar_diario()
        resultado = json.loads(resultado_json)
        return [(diario["glosa"], diario["fecha"]) for diario in resultado]

    def poblar_tabla(self, datos):
        self.tableWidget.setRowCount(len(datos))
        
        for row, (glosa, fecha) in enumerate(datos):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(glosa))

            date_widget = QDateEdit()
            date_widget.setCalendarPopup(True)
            date_widget.setDate(QDate.fromString(fecha, "yyyy-MM-dd"))
            date_widget.setFixedHeight(40)  # 🔹 Asegura que el `QDateEdit` tenga la misma altura en todas las filas
            date_widget.setStyleSheet("""
                QDateEdit {
                    background-color: #1a1a1a;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    border: 1px solid #444;
                    padding: 5px;
                    font-size: 16px; /* 🔹 Asegura que el texto dentro del QDateEdit sea grande */
                }
                QCalendarWidget QWidget {
                    alternate-background-color: #1e1e1e;
                    color: white;
                    border-radius: 5px;
                }
                QCalendarWidget QToolButton {
                    background-color: #1e1e1e;
                    color: white;
                    border-radius: 3px;
                    border: 1px solid #444;
                    padding: 4px;
                    min-width: 45px;
                }
                QCalendarWidget QToolButton::menu-indicator {
                    image: none;
                }
                QCalendarWidget QToolButton:hover {
                    background-color: #0078D7;
                    color: white;
                }
                QCalendarWidget QAbstractItemView:enabled {
                    background-color: #1a1a1a;
                    color: white;
                    selection-background-color: #0078D7;
                    selection-color: white;
                }
                QCalendarWidget QHeaderView::section {
                    background-color: #222;
                    color: white;
                }
                /* 🔹 Corrección específica para el campo del año */
                QCalendarWidget QSpinBox {
                    background-color: #1a1a1a;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 5px;
                    font-size: 14px;
                    min-width: 60px;
                }
                QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
                    width: 14px;
                    height: 14px;
                    border-radius: 2px;
                    border: 1px solid #444;
                    background-color: #222;
                }
                QCalendarWidget QSpinBox::up-button:hover, QCalendarWidget QSpinBox::down-button:hover {
                    background-color: #0078D7;
                }
            """)

            self.tableWidget.setCellWidget(row, 1, date_widget)
            self.tableWidget.setRowHeight(row, 50)  # 🔹 Asegura que todas las filas tengan el mismo tamaño

        self.tableWidget.viewport().update()  # 🔹 Fuerza una actualización visual

    def agregar_fila(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        
        nuevo_item = CustomTableItem("(Nuevo)")
        nuevo_item.setFlags(nuevo_item.flags() | QtCore.Qt.ItemIsEditable)
        self.tableWidget.setItem(row, 0, nuevo_item)

        date_widget = QDateEdit()
        date_widget.setCalendarPopup(True)
        date_widget.setDate(QDate.currentDate())
        self.tableWidget.setCellWidget(row, 1, date_widget)

    def eliminar_fila(self):
        """Elimina la fila seleccionada en la tabla y en la base de datos."""
        row = self.tableWidget.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una fila para eliminar.")
            return

        # Obtener la glosa y la fecha de la fila seleccionada
        item_glosa = self.tableWidget.item(row, 0)
        date_widget = self.tableWidget.cellWidget(row, 1)

        if item_glosa is None or date_widget is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la información de la fila seleccionada.")
            return

        glosa = item_glosa.text()
        fecha = date_widget.date().toString("yyyy-MM-dd")

        # Confirmación antes de eliminar
        confirmacion = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Seguro que desea eliminar el diario con fecha {fecha} y glosa '{glosa}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            if eliminar_diario(fecha, glosa):
                self.tableWidget.removeRow(row)  # Elimina visualmente la fila de la tabla
                QMessageBox.information(self, "Éxito", "📌 Diario eliminado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se ha podido eliminar el diario de la base de datos.")


    def filtrar_tabla(self):
        filtro = self.search_bar.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            if item and filtro in item.text().lower():
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)

    def exportar_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", "", "Archivos CSV (*.csv)")
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write("Glosa,Fecha\n")
                for row in range(self.tableWidget.rowCount()):
                    glosa = self.tableWidget.item(row, 0).text()
                    fecha = self.tableWidget.cellWidget(row, 1).date().toString("yyyy-MM-dd")
                    file.write(f"{glosa},{fecha}\n")
            QMessageBox.information(self, "Éxito", "El archivo CSV ha sido guardado correctamente.")

    def actualizar_estado_boton(self):
        if self.tableWidget.currentRow() >= 0:
            self.btn_view_transaction.setEnabled(True)
        else:
            self.btn_view_transaction.setEnabled(False)

    def actualizar_tabla(self):
        datos = self.obtener_diarios()
        self.poblar_tabla(datos)

    def ver_transaccion(self):
        diarios_disponibles = self.obtener_diarios()

        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione un diario para ver las transacciones.")
            return
        
        glosa = self.tableWidget.item(row, 0).text()
        fecha = self.tableWidget.cellWidget(row, 1).date().toString("yyyy-MM-dd")

        if (glosa, fecha) not in diarios_disponibles:
            QMessageBox.warning(self, "Error", "El diario seleccionado no es válido.")
            return

        self.main_window.stackedWidget.addWidget(Page4(self.main_window, glosa, fecha))
        self.main_window.stackedWidget.setCurrentIndex(self.main_window.stackedWidget.count() - 1)

    def actualizar_diarios(self):
        diarios_originales = self.obtener_diarios()
    
        for row in range(self.tableWidget.rowCount()):
            glosa_item = self.tableWidget.item(row, 0)
            fecha = self.tableWidget.cellWidget(row, 1).date().toString("yyyy-MM-dd")
        
            if glosa_item:
                glosa = glosa_item.text()
            
                if glosa.startswith("(Nuevo)"):
                    glosa = glosa.replace("(Nuevo)", "").strip()
                    try:
                        registrar_diario(fecha, glosa)
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Error al registrar el diario: {str(e)}")
                else:
                    glosa_antigua, fecha_antigua = diarios_originales[row]
                    if glosa != glosa_antigua or fecha != fecha_antigua:
                        try:
                            actualizar_diario(fecha, glosa, fecha_antigua, glosa_antigua)
                        except Exception as e:
                            QMessageBox.warning(self, "Error", f"Error al actualizar el diario: {str(e)}")

        datos = self.obtener_diarios()
        self.poblar_tabla(datos)
        QMessageBox.information(self, "Éxito", "Los diarios han sido actualizados correctamente.")

    def volver_al_inicio(self):
        if self.main_window:
            self.main_window.stackedWidget.setCurrentIndex(0)