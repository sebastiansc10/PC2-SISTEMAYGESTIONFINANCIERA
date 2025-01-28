# gui.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import requests

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle("Mi GUI con PyQt")
        self.setGeometry(100, 100, 300, 200)

        # Crear un layout
        layout = QVBoxLayout()

        # Etiqueta para mostrar el mensaje
        self.label = QLabel("Esperando...", self)
        layout.addWidget(self.label)

        # Botón para hacer una solicitud a la API
        self.button = QPushButton("Obtener Datos de API", self)
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        # Establecer el layout en la ventana principal
        self.setLayout(layout)

    def on_button_click(self):
        # Hacer la solicitud a tu endpoint FastAPI
        response = requests.get("http://127.0.0.1:8000/api/etiquetas")
        if response.status_code == 200:
            # Mostrar los resultados en la etiqueta
            self.label.setText(f"Datos obtenidos: {response.json()}")
        else:
            self.label.setText("Error al obtener los datos")

# Función para ejecutar la aplicación
def run_app():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
