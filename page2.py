import json
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QTableWidgetItem, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFileDialog, QHeaderView, QTableWidget, QWidget,
)
from PyQt5.QtCore import QDate
from app.funciones.DiarioTransaccion import eliminar_diario, mostrar_diario, registrar_diario, actualizar_diario, truncar_diario
from page4 import Page4

# ───────────────── StoneCo Palette (puedes ajustar colores si quieres) ─────────────────
STONE = {
    "bg":          "#0e1113",   # fondo app
    "panel":       "#101417",   # panel derecho
    "sidebar":     "#0b0f12",   # sidebar izquierdo
    "text":        "#ecf1f3",
    "muted":       "#c7d3d9",

    # Verdes corporativos
    "g1":          "#00A859",
    "g2":          "#00C853",
    "g_dark":      "#0a8b4c",
    "g_outline":   "#173028",

    # Acentos / neutros
    "accent":      "#1DE9B6",
    "danger":      "#e74c3c",
    "warning":     "#f39c12",
    "info":        "#2ea3ff",
    "gray":        "#9aa7ad",
    "gray_dark":   "#7a8a91",
    "line":        "#1b2328",
    "line_soft":   "#151d22",
}

# ──────────────────────────────── Page2 (con sidebar) ────────────────────────────────
class Page2(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setup_ui()

    # ============= UI =============
    def setup_ui(self):
        # Layout raíz: Sidebar (izq) + Content (der)
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.setLayout(root)
        self.setStyleSheet(f"background: {STONE['bg']}; color:{STONE['text']};")

        # ------- Sidebar -------
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(270)
        self.sidebar.setStyleSheet(f"""
            QWidget {{
                background: {STONE['sidebar']};
                border-right: 1px solid {STONE['line']};
            }}
        """)
        sb_layout = QVBoxLayout(self.sidebar)
        sb_layout.setContentsMargins(18, 18, 18, 18)
        sb_layout.setSpacing(12)

        # Logotipo / título
        brand = QtWidgets.QLabel("📘 Diarios")
        brand.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        brand.setStyleSheet("font-size: 22px; font-weight: 900; letter-spacing: .5px;")
        sb_layout.addWidget(brand)

        # Línea divisoria
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setStyleSheet(f"color:{STONE['line']}; background:{STONE['line']}; min-height:1px;")
        sb_layout.addWidget(line)

        # Botones de acción (vertical)
        self.btn_add    = self._sidebar_btn("Agregar")
        self.btn_update = self._sidebar_btn("Actualizar")
        self.btn_delete = self._sidebar_btn("Eliminar")
        self.btn_export = self._sidebar_btn("Exportar CSV")
        self.btn_view_transaction = self._sidebar_btn("Ver Transacción")
        self.btn_clear  = self._sidebar_btn("Limpiar Diarios", danger=True)

        for b in (self.btn_add, self.btn_update, self.btn_delete, self.btn_export,
                  self.btn_view_transaction, self.btn_clear):
            sb_layout.addWidget(b)

        sb_layout.addStretch(1)

        # Botón volver pegado abajo
        self.btn_back = self._sidebar_btn("Regresar", secondary=True)
        sb_layout.addWidget(self.btn_back)

        # ------- Contenido derecho -------
        content = QWidget()
        content.setStyleSheet(f"""
            QWidget#content {{
                background: {STONE['panel']};
            }}
        """)
        content.setObjectName("content")
        ct = QVBoxLayout(content)
        ct.setContentsMargins(20, 18, 20, 18)
        ct.setSpacing(14)

        # Header
        header = QWidget()
        hlyt = QHBoxLayout(header)
        hlyt.setContentsMargins(0, 0, 0, 0)
        title = QtWidgets.QLabel("Diarios Registrados")
        title.setStyleSheet(f"font-size: 20px; font-weight: 800; color:{STONE['muted']};")
        hlyt.addWidget(title, 0, QtCore.Qt.AlignLeft)

        # Buscador en header
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar glosa…")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.mousePressEvent = self.clear_table_selection
        self.search_bar.setFixedWidth(420)          
        self.search_bar.setFixedHeight(44)          
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background: #0f1519;
                color: {STONE['text']};
                border: 1px solid {STONE['line']};
                border-radius: 10px;
                padding: 10px 12px;
                font-size: 15px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {STONE['accent']};
                background: #10181d;
            }}
        """)
        self.search_bar.textChanged.connect(self.filtrar_tabla)
        hlyt.addStretch(1)
        hlyt.addWidget(self.search_bar, 0, QtCore.Qt.AlignRight)

        ct.addWidget(header)

        # Tabla en card
        table_card = QtWidgets.QFrame()
        table_card.setStyleSheet(f"""
            QFrame {{
                background: #0f1519;
                border: 1px solid {STONE['line']};
                border-radius: 14px;
            }}
        """)
        tc = QVBoxLayout(table_card)
        tc.setContentsMargins(0, 0, 0, 0)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(["Glosa", "Fecha"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet(f"""
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {STONE['g1']}, stop:1 {STONE['g2']});
                color: {STONE['text']};
                padding: 10px;
                border: 0;
                font-size: 15px; font-weight: 800;
            }}
            QTableWidget {{
                gridline-color: {STONE['line']};
                color: {STONE['text']};
                background: transparent;
                selection-background-color: rgba(0,200,83,.15);
                selection-color: {STONE['text']};
                alternate-background-color: #0e1418;
            }}
            QTableWidget::item {{
                padding: 6px;
            }}
        """)
        tc.addWidget(self.tableWidget)
        ct.addWidget(table_card, 1)

        # Añadir al root
        root.addWidget(self.sidebar)
        root.addWidget(content, 1)

        # Conexiones
        self.btn_add.clicked.connect(self.agregar_fila)
        self.btn_delete.clicked.connect(self.eliminar_fila)
        self.btn_export.clicked.connect(self.exportar_csv)
        self.btn_view_transaction.clicked.connect(self.ver_transaccion)
        self.btn_update.clicked.connect(self.actualizar_diarios)
        self.btn_clear.clicked.connect(self.limpiar_diarios)
        self.btn_back.clicked.connect(self.volver_al_inicio)

        # Cargar datos
        self.actualizar_tabla()

    # ============= Helpers UI =============
    def _sidebar_btn(self, text, primary=False, secondary=False, danger=False):
        btn = QPushButton(text)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        f = btn.font(); f.setPointSize(14); f.setBold(True); btn.setFont(f)
        base = f"""
            QPushButton {{
                text-align: left;
                padding: 12px 14px;
                border-radius: 12px;
                border: 1px solid {STONE['line_soft']};
                background: #0f1519;
                color: {STONE['text']};
            }}
            QPushButton:hover {{
                border: 1px solid {STONE['accent']};
                background: #101b20;
            }}
            QPushButton:pressed {{
                background: #0d1a16;
            }}
        """
        if primary:
            base = f"""
                QPushButton {{
                    text-align: left;
                    padding: 12px 14px;
                    border-radius: 12px;
                    border: 1px solid {STONE['g_outline']};
                    color: {STONE['text']};
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 {STONE['g1']}, stop:1 {STONE['g2']});
                }}
                QPushButton:hover {{ filter: brightness(110%); }}
            """
        if secondary:
            base = f"""
                QPushButton {{
                    text-align: left;
                    padding: 12px 14px;
                    border-radius: 12px;
                    border: 1px solid {STONE['line']};
                    background: #121a1f;
                    color: {STONE['muted']};
                }}
                QPushButton:hover {{ border: 1px solid {STONE['accent']}; }}
            """
        if danger:
            base = f"""
                QPushButton {{
                    text-align: left;
                    padding: 12px 14px;
                    border-radius: 12px;
                    border: 1px solid #3a1c1c;
                    background: #2a1212;
                    color: #ffd9d6;
                }}
                QPushButton:hover {{ border: 1px solid {STONE['danger']}; }}
            """
        btn.setStyleSheet(base)
        return btn

    def _style_calendar_popup(self, de: QDateEdit):
        """Calendario emergente blanco/negro con header limpio."""
        de.setDisplayFormat("dd/MM/yyyy")
        cal = de.calendarWidget()
        cal.setGridVisible(True)
        cal.setFirstDayOfWeek(QtCore.Qt.Monday)
        cal.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        cal.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        cal.setNavigationBarVisible(True)

        prev_btn  = cal.findChild(QtWidgets.QToolButton, "qt_calendar_prevmonth")
        next_btn  = cal.findChild(QtWidgets.QToolButton, "qt_calendar_nextmonth")
        month_btn = cal.findChild(QtWidgets.QToolButton, "qt_calendar_monthbutton")
        year_btn  = cal.findChild(QtWidgets.QToolButton, "qt_calendar_yearbutton")
        for b in (prev_btn, next_btn, month_btn, year_btn):
            if b:
                b.setIcon(QtGui.QIcon())
                b.setMinimumHeight(30)
                b.setCursor(QtCore.Qt.PointingHandCursor)
        if prev_btn: prev_btn.setText("◄"); prev_btn.setToolTip("Mes anterior")
        if next_btn: next_btn.setText("►"); next_btn.setToolTip("Mes siguiente")

        fmt_clear = QtGui.QTextCharFormat()
        cal.setWeekdayTextFormat(QtCore.Qt.Saturday, fmt_clear)
        cal.setWeekdayTextFormat(QtCore.Qt.Sunday,   fmt_clear)

        fmt_today = QtGui.QTextCharFormat()
        fmt_today.setForeground(QtGui.QBrush(QtGui.QColor("#111111")))
        cal.setDateTextFormat(QtCore.QDate.currentDate(), fmt_today)

        cal.setStyleSheet("""
            QCalendarWidget {
                background-color: #ffffff;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #ffffff;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom: 1px solid #E5E7EB;
                min-height: 36px;
            }
            QCalendarWidget QToolButton {
                background: transparent;
                color: #111111;
                font-weight: 700;
                padding: 4px 8px;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #F3F4F6;
                border: 1px solid #E5E7EB;
            }
            QCalendarWidget QTableView QHeaderView::section {
                background-color: #ffffff;
                color: #6B7280;
                border: none;
                padding: 6px 0;
                font-weight: 700;
            }
            QCalendarWidget QTableView {
                outline: 0;
                gridline-color: #E5E7EB;
                selection-background-color: transparent;
                selection-color: #111111;
            }
            QCalendarWidget QAbstractItemView:enabled {
                background: #ffffff;
                color: #111111;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #9CA3AF;
            }
            QCalendarWidget QAbstractItemView::item {
                padding: 6px;
                border-radius: 14px;
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

    # ============= Datos =============
    def obtener_diarios(self):
        resultado_json = mostrar_diario()
        resultado = json.loads(resultado_json)
        return [(diario["glosa"], diario["fecha"]) for diario in resultado]

    # ============= Tabla =============
    def poblar_tabla(self, datos):
        self.tableWidget.setRowCount(len(datos))
        for row, (glosa, fecha) in enumerate(datos):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(glosa))

            container = QWidget()
            lay = QHBoxLayout(container); lay.setContentsMargins(0, 0, 0, 0)
            date_widget = QDateEdit()
            date_widget.setCalendarPopup(True)
            date_widget.setDate(QDate.fromString(fecha, "yyyy-MM-dd"))
            date_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            date_widget.wheelEvent = lambda event: None
            date_widget.setStyleSheet(f"""
                QDateEdit {{
                    background-color: #0f1519;
                    color: {STONE['text']};
                    border: 1px solid {STONE['line']};
                    padding: 6px 10px;
                    font-size: 15px; border-radius: 10px;
                }}
                QDateEdit:focus {{
                    border: 1.5px solid {STONE['accent']};
                }}
            """)
            self._style_calendar_popup(date_widget)
            lay.addWidget(date_widget)
            container.setLayout(lay)

            self.tableWidget.setCellWidget(row, 1, container)
            self.tableWidget.setRowHeight(row, 50)

        self.tableWidget.viewport().update()

    # ============= Acciones =============
    def agregar_fila(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        nuevo_item = QTableWidgetItem("(Nuevo) ")
        nuevo_item.setFlags(nuevo_item.flags() | QtCore.Qt.ItemIsEditable)
        self.tableWidget.setItem(row, 0, nuevo_item)
        self.tableWidget.setCurrentCell(row, 0)
        self.tableWidget.editItem(nuevo_item)

        container = QWidget()
        lay = QHBoxLayout(container); lay.setContentsMargins(6, 6, 6, 6)
        date_widget = QDateEdit()
        date_widget.setCalendarPopup(True)
        date_widget.setDate(QDate.currentDate())
        date_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        date_widget.wheelEvent = lambda event: None
        date_widget.setStyleSheet(f"""
            QDateEdit {{
                background-color: #0f1519;
                color: {STONE['text']};
                border: 1px solid {STONE['line']};
                padding: 6px 10px;
                font-size: 15px; border-radius: 10px;
            }}
            QDateEdit:focus {{
                border: 1.5px solid {STONE['accent']};
            }}
        """)
        self._style_calendar_popup(date_widget)
        lay.addWidget(date_widget)
        container.setLayout(lay)

        self.tableWidget.setCellWidget(row, 1, container)
        self.tableWidget.setRowHeight(row, 50)
        self.tableWidget.viewport().update()

    def eliminar_fila(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una fila para eliminar.")
            return
        item_glosa = self.tableWidget.item(row, 0)
        container = self.tableWidget.cellWidget(row, 1)
        if item_glosa is None or container is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la fila seleccionada.")
            return
        date_widget = container.findChild(QDateEdit)
        if date_widget is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la fecha.")
            return

        glosa = item_glosa.text()
        fecha = date_widget.date().toString("yyyy-MM-dd")
        if QMessageBox.question(self, "Confirmar", f"¿Eliminar {glosa} ({fecha})?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            if eliminar_diario(fecha, glosa):
                self.tableWidget.removeRow(row)
                QMessageBox.information(self, "Éxito", "Diario eliminado.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar en BD.")

    def filtrar_tabla(self):
        filtro = self.search_bar.text().lower()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            self.tableWidget.setRowHidden(row, not (item and filtro in item.text().lower()))

    def exportar_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", "", "Archivos CSV (*.csv)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("Glosa,Fecha\n")
                for row in range(self.tableWidget.rowCount()):
                    glosa = self.tableWidget.item(row, 0).text()
                    container = self.tableWidget.cellWidget(row, 1)
                    if container:
                        date_widget = container.layout().itemAt(0).widget()
                        fecha = date_widget.date().toString("yyyy-MM-dd") if isinstance(date_widget, QDateEdit) else ""
                    else:
                        fecha = ""
                    f.write(f"{glosa},{fecha}\n")
            QMessageBox.information(self, "Éxito", "CSV exportado.")

    def actualizar_estado_boton(self):
        self.btn_view_transaction.setEnabled(self.tableWidget.currentRow() >= 0)

    def actualizar_tabla(self):
        datos = self.obtener_diarios()
        self.poblar_tabla(datos)

    def ver_transaccion(self):
        diarios_disponibles = self.obtener_diarios()
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione un diario.")
            return
        glosa = self.tableWidget.item(row, 0).text()
        container = self.tableWidget.cellWidget(row, 1)
        if container is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la fecha.")
            return
        date_widget = container.findChild(QDateEdit)
        if date_widget is None:
            QMessageBox.warning(self, "Error", "No se pudo obtener la fecha.")
            return
        fecha = date_widget.date().toString("yyyy-MM-dd")
        if (glosa, fecha) not in diarios_disponibles:
            QMessageBox.warning(self, "Error", "El diario seleccionado no es válido.")
            return

        self.main_window.stackedWidget.addWidget(Page4(self.main_window, glosa, fecha))
        self.main_window.stackedWidget.setCurrentIndex(self.main_window.stackedWidget.count() - 1)

    def actualizar_diarios(self):
        originales = self.obtener_diarios()
        cambios = False
        for row in range(self.tableWidget.rowCount()):
            glosa_item = self.tableWidget.item(row, 0)
            container = self.tableWidget.cellWidget(row, 1)
            date_widget = container.findChild(QDateEdit) if container else None
            if not glosa_item or not date_widget:
                continue
            glosa = glosa_item.text().strip()
            fecha = date_widget.date().toString("yyyy-MM-dd")
            if glosa.startswith("(Nuevo)"):
                glosa = glosa.replace("(Nuevo)", "").strip()

            if row >= len(originales):
                try:
                    registrar_diario(fecha, glosa)
                    cambios = True
                    glosa_item.setText(glosa)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Registro: {e}")
            else:
                glosa_old, fecha_old = originales[row]
                if glosa != glosa_old or fecha != fecha_old:
                    try:
                        actualizar_diario(fecha, glosa, fecha_old, glosa_old)
                        cambios = True
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Actualización: {e}")

        if cambios:
            self.poblar_tabla(self.obtener_diarios())
            self.tableWidget.viewport().update()
            QMessageBox.information(self, "Éxito", "Diarios actualizados.")
        else:
            QMessageBox.information(self, "Sin cambios", "No se detectaron modificaciones.")

    def limpiar_diarios(self):
        if QMessageBox.question(
            self, "Confirmar limpieza",
            "⚠️ ¿Eliminar TODOS los diarios? Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        ) == QMessageBox.Yes:
            try:
                resultado = json.loads(truncar_diario())
                if "mensaje" in resultado:
                    QMessageBox.information(self, "Éxito", resultado["mensaje"])
                    self.actualizar_tabla()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo limpiar la tabla.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def clear_table_selection(self, event):
        self.tableWidget.clearSelection()
        QLineEdit.mousePressEvent(self.search_bar, event)

    def volver_al_inicio(self):
        if self.main_window:
            self.main_window.stackedWidget.setCurrentIndex(0)
