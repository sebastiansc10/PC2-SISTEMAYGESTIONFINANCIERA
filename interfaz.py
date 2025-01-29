import json
from PyQt5 import QtCore, QtGui, QtWidgets
from app.funciones.DiarioTransaccion import mostrar_diario  # Importa la función desde base_de_datos

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1001, 751))
        self.stackedWidget.setObjectName("stackedWidget")
        
        # Página 1
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        
        # Botón para cambiar a página 2
        self.input = QtWidgets.QPushButton(self.page)
        self.input.setGeometry(QtCore.QRect(280, 470, 93, 28))
        self.input.setObjectName("input")
        self.output = QtWidgets.QPushButton(self.page)
        self.output.setGeometry(QtCore.QRect(540, 470, 93, 28))
        self.output.setObjectName("output")
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setGeometry(QtCore.QRect(280, 250, 171, 21))
        self.label_2.setObjectName("label_2")
        
        # Conectamos el botón "Ver diarios" a la acción de cambiar de página
        self.input.clicked.connect(self.mostrar_diarios)

        self.stackedWidget.addWidget(self.page)
        
        # Página 2
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setGeometry(QtCore.QRect(400, 40, 55, 16))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget.setGeometry(QtCore.QRect(160, 80, 581, 161))
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.stackedWidget.addWidget(self.page_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.input.setText(_translate("MainWindow", "Ver diarios"))
        self.output.setText(_translate("MainWindow", "Ver reportes"))
        self.label_2.setText(_translate("MainWindow", "Sistema contable"))
        self.label.setText(_translate("MainWindow", "Diarios"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Glosa"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Fecha"))
    
    def mostrar_diarios(self):
        """Función para mostrar la página 2 (diarios)."""
        self.stackedWidget.setCurrentIndex(1)  # Cambiar a la página 2
        # Poblar la tabla con los datos
        datos = self.obtener_diarios()  # Obtener los datos
        self.poblar_tabla(datos)  # Llamar a la función para poblar la tabla

    def obtener_diarios(self):
        """Llama a la función mostrar_diario desde el archivo base_de_datos."""
        resultado_json = mostrar_diario()  # Obtenemos el JSON
        # Convertimos el JSON a un diccionario para obtener las claves y valores
        resultado = json.loads(resultado_json)
        return [(fecha, glosa) for fecha, glosa in resultado.items()]

    def poblar_tabla(self, datos):
        """Llena la tabla con los datos obtenidos."""
        self.tableWidget.setRowCount(len(datos))  # Establecemos el número de filas según los datos
        for row, (fecha, glosa) in enumerate(datos):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(fecha))  # Columna de fecha
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(glosa))  # Columna de glosa


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
