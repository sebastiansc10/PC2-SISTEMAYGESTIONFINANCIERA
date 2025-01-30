import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidgetItem, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFileDialog, QHeaderView, QTableWidget
)
from PyQt5.QtCore import QDate
from app.funciones.DiarioTransaccion import eliminar_diario, mostrar_diario, registrar_diario, actualizar_diario, truncar_diario
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

        self.search_bar.mousePressEvent = self.clear_table_selection

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
            /* 🔹 Fondo General de la Tabla */
            QTableWidget {
                background-color: #121212;
                gridline-color: #444;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }

            /* 🔹 Ítems de la Tabla */
            QTableWidget::item {
                background-color: #1a1a1a;
                color: white;
                padding: 6px;
            }

            /* 🔹 Cabeceras */
            QHeaderView::section {
                background-color: #0078D7;
                color: white;
                padding: 10px;  
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 6px;  /* 🔹 Bordes redondeados */
            }

            /* 🔹 Selección de Items */
            QTableWidget::item:selected {
                background-color: #005A9E;
                color: white;
                border: 2px solid #FFF;
                border-radius: 6px;  /* 🔹 Hace la selección más elegante */
            }

            /* 🔹 Estilo para el Scrollbar */
            QScrollBar:vertical {
                border: none;
                background: #1a1a1a;
                width: 12px; /* 🔹 Hace el scrollbar más delgado */
                margin: 2px 2px 2px 2px;
                border-radius: 6px;
            }

            /* 🔹 Parte del Scrollbar que se mueve */
            QScrollBar::handle:vertical {
                background: #444;
                border-radius: 6px;
                min-height: 20px;
            }
            
            /* 🔹 Cuando el cursor pasa sobre el Scroll */
            QScrollBar::handle:vertical:hover {
                background: #0078D7;
            }
            
            /* 🔹 Cuando se hace clic en el Scroll */
            QScrollBar::handle:vertical:pressed {
                background: #005A9E;
            }

            /* 🔹 Flechas del Scroll */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                width: 0px;
                height: 0px;
            }

            /* 🔹 Espacio entre scrollbar y bordes */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            /* 🔹 QDateEdit para que combine mejor */
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
                background-color: #005A9E;
                color: white;
                border: 2px solid #FFF;
            }
        """)

        self.btn_add = self.create_button("➕ Agregar", "#009688", "#00796B")  # 🔹 Verde oscuro
        self.btn_delete = self.create_button("🗑️ Eliminar", "#e74c3c", "#c0392b")  # 🔹 Rojo oscuro
        self.btn_export = self.create_button("📤 Exportar CSV", "#f39c12", "#d68910")  # 🔹 Naranja oscuro
        self.btn_view_transaction = self.create_button("👁️ Ver Transacción", "#3498db", "#2980b9")  # 🔹 Azul oscuro
        self.btn_update = self.create_button("🔄 Actualizar", "#2ecc71", "#27ae60")  # 🔹 Verde claro
        self.btn_clear = self.create_button("🧹 Limpiar Diarios", "#8e44ad", "#732d91")
        self.btn_back = self.create_button("🏠 Ir al Inicio", "#95a5a6", "#7f8c8d")  # 🔹 Gris oscuro
       

        self.btn_add.clicked.connect(self.agregar_fila)
        self.btn_delete.clicked.connect(self.eliminar_fila)
        self.btn_export.clicked.connect(self.exportar_csv)
        self.btn_view_transaction.clicked.connect(self.ver_transaccion)
        self.btn_update.clicked.connect(self.actualizar_diarios)
        self.btn_clear.clicked.connect(self.limpiar_diarios)
        self.btn_back.clicked.connect(self.volver_al_inicio)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_view_transaction)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_back)
         

        self.page2_layout.addWidget(self.label)
        self.page2_layout.addWidget(self.search_bar)
        self.page2_layout.addWidget(self.tableWidget)
        self.page2_layout.addLayout(btn_layout)
        self.setLayout(self.page2_layout)

        self.actualizar_tabla()

    def clear_table_selection(self, event):
        """Limpia la selección de la tabla cuando se hace clic en la barra de búsqueda."""
        self.tableWidget.clearSelection()
        QLineEdit.mousePressEvent(self.search_bar, event)  # Permite la funcionalidad normal del clic en el cuadro de búsqueda

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

            # 🔹 Contenedor para la fecha
            container_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(container_widget)
            layout.setContentsMargins(0, 0, 0, 0)  # 🔹 Elimina márgenes para que ocupe todo el espacio

            date_widget = QDateEdit()
            date_widget.setCalendarPopup(True)
            date_widget.setDate(QDate.fromString(fecha, "yyyy-MM-dd"))

            # 🔹 Ajustamos su tamaño para que llene la celda completamente
            date_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            date_widget.setMinimumHeight(self.tableWidget.rowHeight(row))

            # 🔹 Bloqueamos el cambio con la rueda del mouse
            date_widget.wheelEvent = lambda event: None

            # 🔹 Estilos para que ocupe bien la celda
            date_widget.setStyleSheet("""
                QDateEdit {
                background-color: #1a1a1a;
                color: white;
                font-weight: bold;
                border: none;
                padding: 6px 0px; /* 🔹 Ajuste vertical */
                font-size: 16px;
                text-align: center;
                }
                QDateEdit::drop-down {
                    width: 20px; /* 🔹 Ajusta el tamaño del icono de flecha */
                    subcontrol-origin: padding;
                    subcontrol-position: right center;
                }
                QAbstractItemView::item {
                    padding: 10px; /* 🔹 Asegura centrado */
                }
            """)

            layout.addWidget(date_widget)  # 🔹 Agregamos el `QDateEdit` al contenedor
            container_widget.setLayout(layout)  # 🔹 Aplicamos el layout al contenedor

            self.tableWidget.setCellWidget(row, 1, container_widget)  # 🔹 Insertamos el contenedor en la celda
            self.tableWidget.setRowHeight(row, max(date_widget.sizeHint().height(), 50))  # 🔹 Asegura que las filas sean uniformes

        self.tableWidget.viewport().update()  # 🔹 Fuerza una actualización visual

    def agregar_fila(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        # 🔹 Crear y configurar la celda de glosa
        nuevo_texto = "(Nuevo) "  # 🔹 Se agrega un espacio después de "(Nuevo) "
        nuevo_item = QTableWidgetItem(nuevo_texto)
        nuevo_item.setFlags(nuevo_item.flags() | QtCore.Qt.ItemIsEditable)
        self.tableWidget.setItem(row, 0, nuevo_item)

        # 🔹 Activar la edición de la celda inmediatamente
        self.tableWidget.setCurrentCell(row, 0)
        self.tableWidget.editItem(nuevo_item)

        # 🔹 Obtener el editor activo de la celda (QLineEdit)
        editor = self.tableWidget.indexWidget(self.tableWidget.currentIndex())

        if isinstance(editor, QtWidgets.QLineEdit):
            editor.setCursorPosition(len(nuevo_texto))  # 🔹 Mueve el cursor al final del texto

        # 🔹 Crear contenedor para la fecha (igual que en poblar_tabla)
        container_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 🔹 Elimina márgenes

        date_widget = QDateEdit()
        date_widget.setCalendarPopup(True)
        date_widget.setDate(QDate.currentDate())
        date_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        date_widget.setMinimumHeight(self.tableWidget.rowHeight(row))  # 🔹 Ajustar altura igual a las demás

        # 🔹 Bloquear scroll con la rueda del mouse
        date_widget.wheelEvent = lambda event: None

        # 🔹 Aplicar el mismo estilo que en poblar_tabla
        date_widget.setStyleSheet("""
            QDateEdit {
                background-color: #1a1a1a;
                color: white;
                font-weight: bold;
                border: none;
                padding: 6px 0px; /* 🔹 Ajuste vertical */
                font-size: 16px;
                text-align: center;
            }
            QDateEdit::drop-down {
                width: 20px;
                subcontrol-origin: padding;
                subcontrol-position: right center;
            }
        """)

        layout.addWidget(date_widget)
        container_widget.setLayout(layout)

        # 🔹 Insertar contenedor en la celda de fecha
        self.tableWidget.setCellWidget(row, 1, container_widget)

        # 🔹 Asegurar que todas las filas mantengan la misma altura
        self.tableWidget.setRowHeight(row, 50)

        self.tableWidget.viewport().update()  # 🔹 Actualizar la tabla

    def eliminar_fila(self):
        """Elimina la fila seleccionada en la tabla y en la base de datos."""
        row = self.tableWidget.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una fila para eliminar.")
            return

        # Obtener la glosa y la fecha de la fila seleccionada
        item_glosa = self.tableWidget.item(row, 0)
        container_widget = self.tableWidget.cellWidget(row, 1)

        if item_glosa is None or container_widget is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la información de la fila seleccionada.")
            return

        # 🔹 Buscar el `QDateEdit` dentro del contenedor
        date_widget = container_widget.findChild(QDateEdit)

        if date_widget is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la fecha del diario seleccionado.")
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

                    # 🔹 Obtener el contenedor de la celda
                    container = self.tableWidget.cellWidget(row, 1)
                    if container:
                        # 🔹 Buscar el QDateEdit dentro del contenedor
                        date_widget = container.layout().itemAt(0).widget()
                        if isinstance(date_widget, QDateEdit):
                            fecha = date_widget.date().toString("yyyy-MM-dd")
                        else:
                            fecha = "Fecha no disponible"
                    else:
                        fecha = "Fecha no disponible"

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
        container_widget = self.tableWidget.cellWidget(row, 1)

        if container_widget is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la fecha del diario seleccionado.")
            return

        # 🔹 Buscar el `QDateEdit` dentro del contenedor
        date_widget = container_widget.findChild(QDateEdit)

        if date_widget is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la fecha del diario seleccionado.")
            return

        fecha = date_widget.date().toString("yyyy-MM-dd")

        if (glosa, fecha) not in diarios_disponibles:
            QMessageBox.warning(self, "Error", "El diario seleccionado no es válido.")
            return

        self.main_window.stackedWidget.addWidget(Page4(self.main_window, glosa, fecha))
        self.main_window.stackedWidget.setCurrentIndex(self.main_window.stackedWidget.count() - 1)

    def actualizar_diarios(self):
        diarios_originales = self.obtener_diarios()
        cambios_realizados = False  # 🔹 Bandera para detectar cambios

        for row in range(self.tableWidget.rowCount()):
            glosa_item = self.tableWidget.item(row, 0)
            container_widget = self.tableWidget.cellWidget(row, 1)
            date_widget = container_widget.findChild(QDateEdit) if container_widget else None

            if not glosa_item or not date_widget:  
                continue  # 🔹 Si falta algún elemento, omitir fila

            glosa = glosa_item.text().strip()
            fecha = date_widget.date().toString("yyyy-MM-dd")

            # 🔹 Verificar si es una fila nueva (tiene "(Nuevo)" al inicio)
            if glosa.startswith("(Nuevo)"):
                glosa = glosa.replace("(Nuevo)", "").strip()  # 🔹 Eliminar "(Nuevo)"

            if row >= len(diarios_originales):  # 🔹 Nueva fila (no estaba en la BD)
                try:
                    registrar_diario(fecha, glosa)  # 🔹 Guardar en BD
                    cambios_realizados = True
                    glosa_item.setText(glosa)  # 🔹 Actualizar el texto sin "(Nuevo)"
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error al registrar el diario: {str(e)}")
            else:
                # 🔹 Datos antiguos en BD
                glosa_antigua, fecha_antigua = diarios_originales[row]

                # 🔹 Si hubo cambios, actualizar en la base de datos
                if glosa != glosa_antigua or fecha != fecha_antigua:
                    try:
                        actualizar_diario(fecha, glosa, fecha_antigua, glosa_antigua)
                        cambios_realizados = True
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Error al actualizar el diario: {str(e)}")

        if cambios_realizados:
            datos = self.obtener_diarios()
            self.poblar_tabla(datos)  # 🔹 Recarga la tabla con los datos actualizados
            self.tableWidget.viewport().update()  # 🔹 Forzar la actualización visual
            QMessageBox.information(self, "Éxito", "Los diarios han sido actualizados correctamente.")
        else:
            QMessageBox.information(self, "Sin cambios", "No se han detectado modificaciones en los diarios.")


    def limpiar_diarios(self):
        """Limpia todos los registros de la tabla Diario y actualiza la interfaz."""
        confirmacion = QMessageBox.question(
            self, "Confirmar limpieza",
            "⚠️ ¿Estás seguro de que deseas eliminar todos los diarios?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            try:
                resultado_json = truncar_diario()  # 🔹 Llama a la función para truncar la tabla
                resultado = json.loads(resultado_json)

                if "mensaje" in resultado:
                    QMessageBox.information(self, "Éxito", resultado["mensaje"])
                    self.actualizar_tabla()  # 🔹 Refresca la tabla para reflejar los cambios
                else:
                    QMessageBox.warning(self, "Error", "No se pudo limpiar la tabla.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Se produjo un error al limpiar la tabla: {str(e)}")


    def volver_al_inicio(self):
        if self.main_window:
            self.main_window.stackedWidget.setCurrentIndex(0)