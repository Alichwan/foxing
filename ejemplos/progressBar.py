import sys
from pprint import pprint
from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication)
from PyQt5.QtCore import QTimer

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(30,40,200,25)

        self.btnStart = QPushButton('Start', self)
        self.btnStart.move(40,80)
        self.btnStart.clicked.connect(self.startProgress)

        self.timer = QTimer()
        self.timer.timeout.connect(self.funcion)
        self.step = 0

    def startProgress(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btnStart.setText('Start')
        else:
            self.timer.start(10)
            self.btnStart.setText('Stop ')

    def funcion(self):
        if self.step >= 100:
            self.timer.stop()
            self.btnStart.setText('Finish')
            return
        self.step += 0.5
        self.progressBar.setValue(self.step)



if __name__ == '__main__':
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())