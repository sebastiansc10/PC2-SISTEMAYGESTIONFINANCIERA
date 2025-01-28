import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMessageBox, QWidget
from PyQt5.QtCore import Qt  # Importar Qt para AlignCenter


# Funciones para los botones
def abrir_diarios():
    QMessageBox.information(None, "Diarios", "Se ha abierto la sección de Diarios")

def calcular():
    QMessageBox.information(None, "Calcular", "Se ha abierto la sección de Calcular")

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
        botones_layout = QHBoxLayout()

        # Botones con flechas
        diarios_button = QPushButton("Diarios")
        diarios_button.clicked.connect(abrir_diarios)
        botones_layout.addWidget(diarios_button)

        flecha1_label = QLabel("➡️")
        flecha1_label.setAlignment(Qt.AlignCenter)
        botones_layout.addWidget(flecha1_label)

        calcular_button = QPushButton("Calcular")
        calcular_button.clicked.connect(calcular)
        botones_layout.addWidget(calcular_button)

        flecha2_label = QLabel("➡️")
        flecha2_label.setAlignment(Qt.AlignCenter)
        botones_layout.addWidget(flecha2_label)

        reporte_button = QPushButton("Reporte")
        reporte_button.clicked.connect(reporte)
        botones_layout.addWidget(reporte_button)

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
