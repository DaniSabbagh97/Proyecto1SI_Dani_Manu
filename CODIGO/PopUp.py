from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 408)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Edicion = QtWidgets.QTextEdit(self.centralwidget)
        self.Edicion.setGeometry(QtCore.QRect(50, 40, 621, 281))
        self.Edicion.setObjectName("Edicion")
        self.Edicion.setDisabled(True)
        self.boton = QtWidgets.QPushButton(self.centralwidget)
        self.boton.setGeometry(QtCore.QRect(470, 320, 141, 51))
        self.boton.setObjectName("boton")
        self.boton.clicked.connect(self.guardarTexto)
        self.boton.setDisabled(True)
        self.cargartexto = QtWidgets.QPushButton(self.centralwidget)
        self.cargartexto.setGeometry(QtCore.QRect(150, 320, 141, 51))
        self.cargartexto.setObjectName("cargartexto")
        self.cargartexto.clicked.connect(self.ponerTexto)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 741, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Sugerir Cambios", "Sugerir Cambios"))
        self.Edicion.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Pulse el boton de cargar texto para que se cargue el texto transcrito</p></body></html>"))
        self.boton.setText(_translate("MainWindow", "OK"))
        self.cargartexto.setText(_translate("MainWindow", "Cargar texto"))

    def ponerTexto(self):
        f = open("temporal.txt", "r")
        content = f.read()
        print(content)
        self.Edicion.setPlainText(content)
        f.close()

        self.boton.setDisabled(False)
        self.cargartexto.setDisabled(True)
        self.Edicion.setDisabled(False)

    def guardarTexto(self):
        textoFinal = self.Edicion.toPlainText()
        file1 = open("temporal.txt", "w+")
        file1.write(textoFinal)
        file1.close()
        self.Edicion.setPlainText("El texto se ha guardado Correctamente, Gracias.\nSi desea guardarlo haga uso del botón de guardar cambios en la Ventana Principal\nPara salir de la Ventana, haz click en la X de la esquina derecha")
        self.cargartexto.setDisabled(True)
        self.boton.setDisabled(True)
        self.Edicion.setDisabled(True)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
