import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox, QWidget, QDateEdit, QDialog
from PyQt5.QtCore import Qt, QDate  # Importar Qt para AlignCenter y QDate para las fechas

# Funciones para los botones
def abrir_diarios():
    QMessageBox.information(None, "Diarios", "Se ha abierto la sección de Diarios")

def calcular():
    # Crear ventana secundaria para las fechas (ahora usaremos QDialog)
    ventana_calcular = QDialog()
    ventana_calcular.setWindowTitle("Generar Reporte")
    ventana_calcular.setGeometry(200, 200, 400, 200)

    # Crear el layout de la ventana secundaria
    layout_calcular = QVBoxLayout()

    # Etiqueta y campo de fecha inicial
    fecha_inicial_label = QLabel("Fecha inicial:")
    fecha_inicial = QDateEdit()
    fecha_inicial.setDate(QDate.currentDate())  # Establece la fecha actual por defecto
    fecha_inicial.setCalendarPopup(True)  # Mostrar el calendario al hacer clic en el campo
    layout_calcular.addWidget(fecha_inicial_label)
    layout_calcular.addWidget(fecha_inicial)

    # Etiqueta y campo de fecha de cierre
    fecha_cierre_label = QLabel("Fecha de cierre:")
    fecha_cierre = QDateEdit()
    fecha_cierre.setDate(QDate.currentDate())  # Establece la fecha actual por defecto
    fecha_cierre.setCalendarPopup(True)  # Mostrar el calendario al hacer clic en el campo
    layout_calcular.addWidget(fecha_cierre_label)
    layout_calcular.addWidget(fecha_cierre)

    # Botón para generar reporte
    generar_button = QPushButton("Generar Reportes")
    generar_button.clicked.connect(lambda: generar_reporte(fecha_inicial.date(), fecha_cierre.date(), ventana_calcular))
    layout_calcular.addWidget(generar_button)

    # Establecer el layout y mostrar la ventana
    ventana_calcular.setLayout(layout_calcular)
    ventana_calcular.exec_()  # Usamos exec_() para que la ventana se quede abierta hasta que se cierre

def generar_reporte(fecha_inicial, fecha_cierre, ventana_calcular):
    # Aquí puedes añadir la lógica para generar el reporte con las fechas seleccionadas
    QMessageBox.information(None, "Generar Reportes", f"Reportes generados desde {fecha_inicial.toString()} hasta {fecha_cierre.toString()}")
    
    # Mostrar el mensaje de confirmación y luego cerrar la ventana
    QMessageBox.information(None, "Reporte generado", "Reporte generado, para verlos seleccione la opción 'Reportes'")
    
    # Cerrar la ventana de cálculo
    ventana_calcular.close()

def reporte():
    QMessageBox.information(None, "Reporte", "Se ha abierto la sección de Reporte")

# Ventana principal
class SistemaContable(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar ventana
        self.setWindowTitle("Sistema contable")
        self.setGeometry(100, 100, 400, 300)

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Título
        titulo_label = QLabel("Sistema contable")
        titulo_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        titulo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo_label)

        # Layout para botones y flechas
        botones_layout = QVBoxLayout()  # Usamos QVBoxLayout para poner los botones en vertical centrados

        # Botón Diarios
        diarios_button = QPushButton("Diarios")
        diarios_button.clicked.connect(abrir_diarios)
        diarios_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        botones_layout.addWidget(diarios_button, alignment=Qt.AlignCenter)

        # Flecha 1
        flecha1_label = QLabel("➡️")
        flecha1_label.setAlignment(Qt.AlignCenter)
        botones_layout.addWidget(flecha1_label)

        # Botón Calcular
        calcular_button = QPushButton("Calcular")
        calcular_button.clicked.connect(calcular)
        calcular_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        botones_layout.addWidget(calcular_button, alignment=Qt.AlignCenter)

        # Flecha 2
        flecha2_label = QLabel("➡️")
        flecha2_label.setAlignment(Qt.AlignCenter)
        botones_layout.addWidget(flecha2_label)

        # Botón Reporte
        reporte_button = QPushButton("Reporte")
        reporte_button.clicked.connect(reporte)
        reporte_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        botones_layout.addWidget(reporte_button, alignment=Qt.AlignCenter)

        # Agregar los botones al layout principal
        main_layout.addLayout(botones_layout)

        # Crear un widget central y configurar el layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

# Ejecutar aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SistemaContable()
    ventana.show()
    sys.exit(app.exec_())
