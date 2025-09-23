import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QWidget, QFrame, QStackedWidget
)
from PyQt5.QtGui import QColor, QBrush

from app.funciones.EstadoSituacion import (
    calcularbalance, total_debe, total_haber,
    situacion_activocorriente, situacion_totalactivocorriente,
    situacion_pasivo, situacion_totalpasivo,
    situacion_activonocorriente, situacion_totalactivonocorriente,
    situacion_patrimonio
)
from app.funciones.EstadoResultados import calcular_estado_resultados, utilidadantes
from app.funciones.DiarioTransaccion import diariotransaccion
from app.funciones.Mayorizar_BalanceComprobación import mayorizartransacciones

# ──────────────────────────────────────────────────────────────────────────────
STONE = {
    "bg":          "#0e1113",
    "panel":       "#101417",
    "card":        "#0f1519",
    "text":        "#ecf1f3",
    "muted":       "#c7d3d9",
    "line":        "#1b2328",
    "line_soft":   "#151d22",

    "g1":          "#00A859",
    "g2":          "#00C853",
    "g_dark":      "#0a8b4c",
    "g_outline":   "#173028",

    "accent":      "#1DE9B6",
    "gray":        "#9aa7ad",
    "gray_dark":   "#7a8a91",
}

NAV_STYLE = f"""
QPushButton {{
    text-align: left;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid {STONE['line_soft']};
    background: {STONE['card']};
    color: {STONE['text']};
}}
QPushButton:hover {{
    border: 1px solid {STONE['accent']};
    background: #101b20;
}}
"""

NAV_ACTIVE_STYLE = f"""
QPushButton {{
    text-align: left;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid {STONE['g_outline']};
    color: {STONE['text']};
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {STONE['g1']}, stop:1 {STONE['g2']});
}}
"""
# ──────────────────────────────────────────────────────────────────────────────

class Page3(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self._fecha_inicio = None
        self._fecha_fin = None
        self.active_btn = None
        self.setup_ui()

    # ───────────────────────── Helpers ─────────────────────────
    def _set_active_btn(self, btn: QPushButton):
        if self.active_btn and self.active_btn is not btn:
            self.active_btn.setStyleSheet(NAV_STYLE)
        btn.setStyleSheet(NAV_ACTIVE_STYLE)
        self.active_btn = btn

    def _nav_btn(self, text):
        btn = QPushButton(text)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        f = btn.font(); f.setPointSize(8); f.setBold(True); btn.setFont(f)
        btn.setStyleSheet(NAV_STYLE)
        return btn

    def style_table(self, table: QTableWidget):
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {STONE['card']};
                color: {STONE['text']};
                gridline-color: {STONE['line']};
                border: 1px solid {STONE['line']};
                border-radius: 10px;
                selection-background-color: rgba(0,200,83,.15);
                selection-color: {STONE['text']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {STONE['g1']}, stop:1 {STONE['g2']});
                color: {STONE['text']};
                padding: 8px 10px;
                border: none;
                font-weight: 800;
            }}
            QTableWidget::item {{ padding: 6px; }}
        """)

    def _card(self, widget: QWidget) -> QFrame:
        """Card sin padding interno para que la tabla ocupe TODO."""
        card = QFrame()
        card.setStyleSheet(
            f"QFrame{{background:{STONE['panel']}; border:1px solid {STONE['line']}; border-radius:14px;}}"
        )
        lay = QVBoxLayout(card)
        lay.setContentsMargins(0, 0, 0, 0)   # sin padding interno
        lay.setSpacing(0)
        lay.addWidget(widget)
        card.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return card

    def _autosize(self, table: QTableWidget):
        """Hace que la tabla llene la card verticalmente (sin scroll ni huecos)."""
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        h = table.horizontalHeader().height()
        for r in range(table.rowCount()):
            h += table.rowHeight(r)
        h += 2  # pequeño margen visual

        table.setMinimumHeight(h)
        table.setMaximumHeight(h)  # fija el alto para llenar la card
        table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        parent = table.parentWidget()
        if isinstance(parent, QFrame):
            parent.setMinimumHeight(h)
            parent.setMaximumHeight(h)

    # ──────────────────────────── UI ────────────────────────────
    def setup_ui(self):
        self.setStyleSheet(f"background:{STONE['bg']}; color:{STONE['text']};")
        root = QHBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        # Sidebar
        sidebar = QWidget(); sidebar.setFixedWidth(260)
        sidebar.setStyleSheet(f"background:{STONE['panel']}; border-right:1px solid {STONE['line']};")
        sb = QVBoxLayout(sidebar); sb.setContentsMargins(18,18,18,18); sb.setSpacing(10)

        brand = QtWidgets.QLabel("📊 Reportes Contables")
        brand.setStyleSheet("font-size:16px; font-weight:900;")
        sb.addWidget(brand)

        line = QFrame(); line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background:{STONE['line']}; min-height:1px;")
        sb.addWidget(line)

        self.btn_diarios    = self._nav_btn("Diarios y transacción")
        self.btn_mayor      = self._nav_btn("Mayorización")
        self.btn_balanza    = self._nav_btn("Balanza de comprobación")
        self.btn_situacion  = self._nav_btn("Estado de situación financiera")
        self.btn_resultados = self._nav_btn("Estado de resultados")
        for b in (self.btn_diarios, self.btn_mayor, self.btn_balanza, self.btn_situacion, self.btn_resultados):
            sb.addWidget(b)
        sb.addStretch(1)
        self.btn_volver = self._nav_btn("Regresar al inicio")
        sb.addWidget(self.btn_volver)

        # Contenido
        content = QWidget(); content.setStyleSheet(f"background:{STONE['bg']};")
        cv = QVBoxLayout(content)
        cv.setContentsMargins(20, 4, 20, 8)  # MUCHO menos aire
        cv.setSpacing(2)

        self.title = QtWidgets.QLabel("Registros contables")
        self.title.setStyleSheet("font-size:20px; font-weight:900;")
        self.subtitle = QtWidgets.QLabel("Desde 2009-04-01 hasta 2025-09-23")
        self.subtitle.setStyleSheet("font-size:16px; color:#c7d3d9;")

        header = QVBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)  # pegado
        header.setSpacing(0)
        header.addWidget(self.title)
        header.addWidget(self.subtitle)
        cv.addLayout(header)

        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.stack.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Página: Diarios
        diarios_page = QWidget(); dl = QVBoxLayout(diarios_page)
        dl.setContentsMargins(0,0,0,0); dl.setSpacing(6)
        self.diarios_scroll = QScrollArea(); self.diarios_scroll.setWidgetResizable(True)
        self.diarios_scroll.setStyleSheet(f"QScrollArea{{border:1px solid {STONE['line']}; border-radius:14px;}}")
        self.diarios_content = QWidget()
        self.diarios_layout = QVBoxLayout(self.diarios_content); self.diarios_layout.setSpacing(8)
        self.diarios_layout.setContentsMargins(8,8,8,8)
        self.diarios_scroll.setWidget(self.diarios_content)
        dl.addWidget(self.diarios_scroll)

        # Página: Mayorización
        mayor_page = QWidget(); ml = QVBoxLayout(mayor_page)
        ml.setContentsMargins(0,0,0,0); ml.setSpacing(6)
        self.mayor_scroll = QScrollArea(); self.mayor_scroll.setWidgetResizable(True)
        self.mayor_scroll.setStyleSheet(f"QScrollArea{{border:1px solid {STONE['line']}; border-radius:14px;}}")
        self.mayor_content = QWidget()
        self.mayorizacion_layout = QVBoxLayout(self.mayor_content); self.mayorizacion_layout.setSpacing(8)
        self.mayorizacion_layout.setContentsMargins(8,8,8,8)
        self.mayor_scroll.setWidget(self.mayor_content)
        ml.addWidget(self.mayor_scroll)

        # Página: Balanza de comprobación
        balanza_page = QWidget(); bl = QVBoxLayout(balanza_page)
        bl.setContentsMargins(0,0,0,0); bl.setSpacing(0)
        self._tbl_balance = self.crear_tabla_generica(4, ["Código de cuenta", "Nombre de la cuenta", "Debe", "Haber"])
        self.tabla_balance = self._card(self._tbl_balance)
        bl.addWidget(self.tabla_balance)

        # Página: Situación financiera (sin márgenes; ocupa todo)
        situacion_page = QWidget(); sl = QVBoxLayout(situacion_page)
        sl.setContentsMargins(0,0,0,0); sl.setSpacing(0)

        cols = QHBoxLayout()
        cols.setContentsMargins(0, 0, 0, 0)
        cols.setSpacing(10)

        col_izq = QVBoxLayout(); col_izq.setSpacing(10)
        col_der = QVBoxLayout(); col_der.setSpacing(10)

        self._tbl_ac = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
        self._tbl_anc = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
        self.tabla_activo_corriente = self._card(self._tbl_ac)
        self.tabla_activo_no_corriente = self._card(self._tbl_anc)
        col_izq.addWidget(self.tabla_activo_corriente)
        col_izq.addWidget(self.tabla_activo_no_corriente)

        self._tbl_pas = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
        self._tbl_patr = self.crear_tabla_generica(2, ["Cuenta", "Saldo"])
        self.tabla_pasivos = self._card(self._tbl_pas)
        self.tabla_patrimonio = self._card(self._tbl_patr)
        col_der.addWidget(self.tabla_pasivos)
        col_der.addWidget(self.tabla_patrimonio)

        cols.addLayout(col_izq, 1)
        cols.addLayout(col_der, 1)
        sl.addLayout(cols)

        self._tbl_res = self.crear_tabla_generica(4, ["Activo total", "Valor", "Total pasivo + patrimonio", "Valor"])
        self.tabla_resumen = self._card(self._tbl_res)
        sl.addWidget(self.tabla_resumen)

        # Página: Estado de resultados (pegado al subtítulo)
        resultados_page = QWidget(); rl = QVBoxLayout(resultados_page)
        rl.setContentsMargins(0,0,0,0); rl.setSpacing(0)
        self._tbl_resul = self.crear_tabla_generica(3, ["Cuenta", "Monto", "Porcentaje del total"])
        self.tabla_resultados = self._card(self._tbl_resul)
        rl.addWidget(self.tabla_resultados, 0, QtCore.Qt.AlignTop)

        # Añadir al stack
        self.stack.addWidget(diarios_page)     # 0
        self.stack.addWidget(mayor_page)       # 1
        self.stack.addWidget(balanza_page)     # 2
        self.stack.addWidget(situacion_page)   # 3
        self.stack.addWidget(resultados_page)  # 4

        cv.addWidget(self.stack, 1)

        root.addWidget(sidebar)
        root.addWidget(content, 1)

        # Navegación
        self.btn_diarios.clicked.connect(lambda: self.mostrar("diarios"))
        self.btn_mayor.clicked.connect(lambda: self.mostrar("mayor"))
        self.btn_balanza.clicked.connect(lambda: self.mostrar("balanza"))
        self.btn_situacion.clicked.connect(lambda: self.mostrar("situacion"))
        self.btn_resultados.clicked.connect(lambda: self.mostrar("resultados"))
        self.btn_volver.clicked.connect(self.volver_al_inicio)

        # Default
        self.mostrar("diarios")

    # ───────────────────── Tablas base ─────────────────────
    def crear_tabla_generica(self, num_columnas, headers):
        tabla = QTableWidget()
        tabla.setColumnCount(num_columnas)
        tabla.setHorizontalHeaderLabels(headers)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabla.verticalHeader().setVisible(False)
        tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tabla.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        tabla.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        tabla.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.style_table(tabla)
        return tabla

    # ───────────────────────── Actualizaciones ─────────────────────────
    def actualizar_fechas(self, fecha_inicio, fecha_fin):
        self._fecha_inicio, self._fecha_fin = fecha_inicio, fecha_fin
        self.subtitle.setText(f"Desde {fecha_inicio} hasta {fecha_fin}")
        self._refrescar_por_index(self.stack.currentIndex())

    def mostrar(self, section: str):
        mapping = {"diarios":0, "mayor":1, "balanza":2, "situacion":3, "resultados":4}
        btn_map = {
            0: self.btn_diarios, 1: self.btn_mayor, 2: self.btn_balanza,
            3: self.btn_situacion, 4: self.btn_resultados
        }
        idx = mapping.get(section, 0)
        self.stack.setCurrentIndex(idx)

        titles = {
            0:"Diarios y transacción", 1:"Mayorización",
            2:"Balanza de comprobación", 3:"Estado de situación financiera",
            4:"Estado de resultados"
        }
        self.title.setText(titles[idx])
        self._set_active_btn(btn_map[idx])
        self._refrescar_por_index(idx)

    def _refrescar_por_index(self, idx:int):
        if not (self._fecha_inicio and self._fecha_fin):
            return
        if idx == 0:
            self.actualizar_diarios(self._fecha_inicio, self._fecha_fin)
        elif idx == 1:
            self.actualizar_mayorizacion(self._fecha_inicio, self._fecha_fin)
        elif idx == 2:
            self.actualizar_tabla_balance(self._fecha_inicio, self._fecha_fin)
        elif idx == 3:
            self.actualizar_tabla_activo_corriente(self._fecha_inicio, self._fecha_fin)
            self.actualizar_tabla_activo_no_corriente(self._fecha_inicio, self._fecha_fin)
            self.actualizar_tabla_pasivos(self._fecha_inicio, self._fecha_fin)
            self.actualizar_tabla_patrimonio(self._fecha_inicio, self._fecha_fin)
            self.actualizar_tabla_resumen(self._fecha_inicio, self._fecha_fin)
        elif idx == 4:
            self.actualizar_tabla_resultados(self._fecha_inicio, self._fecha_fin)

    # ─────────────────────── BALANZA ───────────────────────
    def actualizar_tabla_balance(self, fi, ff):
        balance_data = json.loads(calcularbalance(fi, ff))
        table = self._tbl_balance
        table.clearContents()
        table.setRowCount(len(balance_data) + 1)

        for row, item in enumerate(balance_data):
            table.setItem(row, 0, QTableWidgetItem(str(item['id_cuenta'])))
            table.setItem(row, 1, QTableWidgetItem(item['nombre_cuenta']))
            table.setItem(row, 2, QTableWidgetItem(f"{item['debe']:.2f}"))
            table.setItem(row, 3, QTableWidgetItem(f"{item['haber']:.2f}"))

        last = len(balance_data)
        table.setSpan(last, 0, 1, 2)
        ti = QTableWidgetItem("Total:"); ti.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        table.setItem(last, 0, ti)
        table.setItem(last, 2, QTableWidgetItem(f"{total_debe(fi, ff):.2f}"))
        table.setItem(last, 3, QTableWidgetItem(f"{total_haber(fi, ff):.2f}"))
        self._autosize(table)

    # ─────────────────── RESULTADOS ───────────────────
    def actualizar_tabla_resultados(self, fi, ff):
        rd = json.loads(calcular_estado_resultados(fi, ff))
        datos = [
            ("Ventas", rd["ventas"]),
            ("Costo de ventas", rd["costo_ventas"]),
            ("Utilidad bruta", rd["utilidad_bruta"]),
            ("Gastos de personal", rd["Gastos de personal"]),
            ("Gastos de servicios", rd["Gastos de servicios"]),
            ("Devaluación", rd["Devaluación"]),
            ("Total gastos operativos", rd["gastos_operativos"]),
            ("Utilidad operativa", rd["utilidad_operativa"]),
            ("Otros ingresos", rd["otros_ingresos"]),
            ("Pérdidas", rd["perdidas"]),
            ("Utilidad antes de impuestos", rd["utilidad_antes_impuestos"]),
            ("Impuesto a la renta", rd["impuesto_renta"]),
            ("Utilidad neta", rd["utilidad_neta"])
        ]
        datos = [d for d in datos if d[1] not in ("", 0)]
        ventas = next((m for n, m in datos if n == "Ventas"), 0)

        table = self._tbl_resul
        table.clearContents(); table.setRowCount(len(datos))

        for r, (nombre, valor) in enumerate(datos):
            it0 = QTableWidgetItem(nombre); it0.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            table.setItem(r, 0, it0)
            it1 = QTableWidgetItem(f"{valor:.2f}"); it1.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            table.setItem(r, 1, it1)
            pct = (valor/ventas*100) if (ventas and isinstance(valor,(int,float))) else 0
            it2 = QTableWidgetItem(f"{pct:.2f}%"); it2.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            table.setItem(r, 2, it2)

        # 1ra col se estira; números a contenido
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        table.horizontalHeader().setStretchLastSection(False)

        self._resaltar_fila(table, "Utilidad bruta", QColor(0, 200, 120))
        self._resaltar_fila(table, "Utilidad operativa", QColor(0, 200, 120))
        self._resaltar_fila(table, "Utilidad antes de impuestos", QColor(0, 170, 100))
        self._autosize(table)

    def _resaltar_fila(self, table: QTableWidget, nombre, color):
        for r in range(table.rowCount()):
            it = table.item(r, 0)
            if it and it.text() == nombre:
                for c in range(table.columnCount()):
                    cell = table.item(r, c)
                    if cell:
                        cell.setBackground(QBrush(color))
                        cell.setForeground(QBrush(QColor(0, 0, 0)))
                break

    # ─────────────────── SITUACIÓN ───────────────────
    def actualizar_tabla_activo_corriente(self, fi, ff):
        data = json.loads(situacion_activocorriente(fi, ff))
        t = self._tbl_ac
        t.clearContents(); t.setRowCount(len(data) + 2)
        t.setSpan(0, 0, 1, 2); t.setItem(0, 0, self._center("Activo corriente"))
        for r, it in enumerate(data, start=1):
            t.setItem(r, 0, QTableWidgetItem(it['nombre_cuenta']))
            t.setItem(r, 1, QTableWidgetItem(f"{it['saldo']:.2f}"))
        total = json.loads(situacion_totalactivocorriente(fi, ff))['Total_Saldo']
        last = len(data) + 1
        t.setItem(last, 0, QTableWidgetItem("Total activo corriente"))
        t.setItem(last, 1, QTableWidgetItem(f"{total:.2f}"))
        self._tot_row_color(t, last); self._autosize(t)

    def actualizar_tabla_activo_no_corriente(self, fi, ff):
        data = json.loads(situacion_activonocorriente(fi, ff))
        t = self._tbl_anc
        t.clearContents(); t.setRowCount(len(data) + 2)
        t.setSpan(0, 0, 1, 2); t.setItem(0, 0, self._center("Activo no corriente"))
        for r, it in enumerate(data, start=1):
            t.setItem(r, 0, QTableWidgetItem(it['nombre_cuenta']))
            t.setItem(r, 1, QTableWidgetItem(f"{it['saldo']:.2f}"))
        total = json.loads(situacion_totalactivonocorriente(fi, ff))['Total_Saldo']
        last = len(data) + 1
        t.setItem(last, 0, QTableWidgetItem("Total activo no corriente"))
        t.setItem(last, 1, QTableWidgetItem(f"{total:.2f}"))
        self._tot_row_color(t, last); self._autosize(t)

    def actualizar_tabla_pasivos(self, fi, ff):
        data = json.loads(situacion_pasivo(fi, ff))
        t = self._tbl_pas
        t.clearContents(); t.setRowCount(len(data) + 2)
        t.setSpan(0, 0, 1, 2); t.setItem(0, 0, self._center("Pasivos"))
        for r, it in enumerate(data, start=1):
            t.setItem(r, 0, QTableWidgetItem(it['nombre_cuenta']))
            t.setItem(r, 1, QTableWidgetItem(f"{it['saldo']:.2f}"))
        total = json.loads(situacion_totalpasivo(fi, ff))['Total_Saldo']
        last = len(data) + 1
        t.setItem(last, 0, QTableWidgetItem("Total pasivos"))
        t.setItem(last, 1, QTableWidgetItem(f"{total:.2f}"))
        self._tot_row_color(t, last); self._autosize(t)

    def actualizar_tabla_patrimonio(self, fi, ff):
        data = json.loads(situacion_patrimonio(fi, ff))
        util = json.loads(utilidadantes(fi, ff))['utilidad_antes_impuestos']
        t = self._tbl_patr
        t.clearContents(); t.setRowCount(len(data) + 3)
        t.setSpan(0, 0, 1, 2); t.setItem(0, 0, self._center("Patrimonio"))
        total_p = 0
        for r, it in enumerate(data, start=1):
            t.setItem(r, 0, QTableWidgetItem(it['nombre_cuenta']))
            t.setItem(r, 1, QTableWidgetItem(f"{it['saldo']:.2f}"))
            total_p += it['saldo']
        r = len(data) + 1
        t.setItem(r, 0, QTableWidgetItem("Utilidades acumuladas"))
        t.setItem(r, 1, QTableWidgetItem(f"{util:.2f}"))
        for c in range(2):
            cell = t.item(r, c)
            if cell:
                cell.setBackground(QBrush(QColor(255, 180, 80)))
                cell.setForeground(QBrush(QColor(0, 0, 0)))
        total_p += util
        r = len(data) + 2
        t.setItem(r, 0, QTableWidgetItem("Total patrimonio"))
        t.setItem(r, 1, QTableWidgetItem(f"{total_p:.2f}"))
        self._tot_row_color(t, r); self._autosize(t)

    def actualizar_tabla_resumen(self, fi, ff):
        ac  = json.loads(situacion_totalactivocorriente(fi, ff))['Total_Saldo']
        anc = json.loads(situacion_totalactivonocorriente(fi, ff))['Total_Saldo']
        pas = json.loads(situacion_totalpasivo(fi, ff))['Total_Saldo']
        patr = sum(x['saldo'] for x in json.loads(situacion_patrimonio(fi, ff)))
        util = json.loads(utilidadantes(fi, ff))['utilidad_antes_impuestos']
        patr += util
        activo_total = ac + anc
        pasivo_patr = pas + patr

        t = self._tbl_res
        t.clearContents(); t.setRowCount(1)
        t.setItem(0, 0, QTableWidgetItem("Activo total"))
        t.setItem(0, 1, QTableWidgetItem(f"{activo_total:.2f}"))
        t.setItem(0, 2, QTableWidgetItem("Total pasivo + patrimonio"))
        t.setItem(0, 3, QTableWidgetItem(f"{pasivo_patr:.2f}"))
        for c in range(4):
            cell = t.item(0, c)
            if cell:
                cell.setBackground(QBrush(QColor(0, 200, 120)))
                cell.setForeground(QBrush(QColor(0, 0, 0)))
        self._autosize(t)

    # ─────────────────── Diarios / Mayor ───────────────────
    def actualizar_diarios(self, fi, ff):
        cont = self.diarios_layout
        while cont.count():
            item = cont.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        diarios = json.loads(diariotransaccion(fi, ff))
        for d in diarios:
            fecha_card = QtWidgets.QLabel(d['fecha'])
            fecha_card.setStyleSheet(f"""
                background:{STONE['card']}; color:{STONE['text']};
                border:1px solid {STONE['line']}; border-radius:10px;
                padding:8px 10px; font-weight:800;
            """)
            cont.addWidget(fecha_card)

            tbl = self.crear_tabla_generica(4, ["Código de cuenta", "Nombre de cuenta", "Debe", "Haber"])
            tbl.setRowCount(len(d['transacciones']))
            for r, t in enumerate(d['transacciones']):
                tbl.setItem(r, 0, QTableWidgetItem(str(t['id_cuenta'])))
                tbl.setItem(r, 1, QTableWidgetItem(t['nombre_cuenta']))
                if t['dh'] == 'Debe':
                    tbl.setItem(r, 2, QTableWidgetItem(f"{t['cantidad']:.2f}"))
                    tbl.setItem(r, 3, QTableWidgetItem("0.00"))
                else:
                    tbl.setItem(r, 2, QTableWidgetItem("0.00"))
                    tbl.setItem(r, 3, QTableWidgetItem(f"{t['cantidad']:.2f}"))
            self._autosize(tbl)
            cont.addWidget(tbl)

            glosa = QtWidgets.QLabel(f"Glosa: {d['glosa']}")
            glosa.setStyleSheet("""
                background:#e8edf0; color:#0e1113;
                border:1px dashed #c3cbd1; border-radius:10px;
                padding:6px 10px; font-style:italic;
            """)
            cont.addWidget(glosa)
            cont.addSpacing(6)

    def actualizar_mayorizacion(self, fi, ff):
        cont = self.mayorizacion_layout
        while cont.count():
            item = cont.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        data = json.loads(mayorizartransacciones(fi, ff))
        cuentas = {}
        for t in data:
            cuentas.setdefault((t['id_cuenta'], t['nombre_cuenta']), []).append(t)

        for (idc, nom), trans in cuentas.items():
            title = QtWidgets.QLabel(f"{idc} - {nom}")
            title.setStyleSheet("color:#bff5d2; font-weight:700; font-size:14px; padding:6px;")
            cont.addWidget(title)

            tbl = self.crear_tabla_generica(3, ["Fecha", "Debe", "Haber"])
            tbl.setRowCount(len(trans) + 1)
            debe = haber = 0
            for r, t in enumerate(trans):
                tbl.setItem(r, 0, QTableWidgetItem(t['fecha']))
                if t['dh'] == 'Debe':
                    tbl.setItem(r, 1, QTableWidgetItem(f"{t['cantidad']:.2f}")); tbl.setItem(r, 2, QTableWidgetItem("0.00"))
                    debe += t['cantidad']
                else:
                    tbl.setItem(r, 1, QTableWidgetItem("0.00")); tbl.setItem(r, 2, QTableWidgetItem(f"{t['cantidad']:.2f}"))
                    haber += t['cantidad']
            last = len(trans)
            saldo = debe - haber
            it = QTableWidgetItem("Saldo"); it.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            tbl.setItem(last, 0, it)
            if saldo >= 0:
                tbl.setItem(last, 1, QTableWidgetItem(f"{abs(saldo):.2f}")); tbl.setItem(last, 2, QTableWidgetItem("0.00"))
            else:
                tbl.setItem(last, 1, QTableWidgetItem("0.00")); tbl.setItem(last, 2, QTableWidgetItem(f"{abs(saldo):.2f}"))
            self._autosize(tbl)
            cont.addWidget(tbl)

    # ─────────────────── Util ───────────────────
    def _center(self, text):
        it = QTableWidgetItem(text); it.setTextAlignment(QtCore.Qt.AlignCenter); return it

    def _tot_row_color(self, t: QTableWidget, row: int):
        for c in range(t.columnCount()):
            cell = t.item(row, c)
            if cell:
                cell.setBackground(QBrush(QColor(0, 200, 120)))
                cell.setForeground(QBrush(QColor(0, 0, 0)))

    def volver_al_inicio(self):
        if self.parent_window:
            self.parent_window.stackedWidget.setCurrentIndex(0)
