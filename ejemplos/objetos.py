"""Basado en ejemplo de Mr.Patiwi de 2016-1"""
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QDesktopWidget
from PyQt5.QtGui import QPixmap
import sys
import time
from math import sin, cos, pi


class MoveMyImageEvent:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class Personaje(QThread):
    trigger = pyqtSignal(MoveMyImageEvent)

    def __init__(self, parent, x, y):
        super().__init__()
        self.image = QLabel(parent)
        self.image.setGeometry(100, 100, 100, 100)
        self.image.setPixmap(QPixmap("personaje_0.png"))
        self.image.show()
        self.image.setVisible(True)
        self.trigger.connect(parent.actualizar_imagen)
        self.__position = (0, 0)
        self.position = (x, y)
        self.mover = False
        self.velocidad = 2
        self.velocidad_giro = 0
        self.orientacion = 0

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(MoveMyImageEvent(self.image, self.position[0], self.position[1]))

    def run(self):
        while True:
            time.sleep(0.02)

            self.orientacion += self.velocidad_giro
            print(self.orientacion)
            if self.mover:
                if self.position[1] <= 500:
                    self.position = (self.position[0] + self.velocidad * cos(self.orientacion),
                                     self.position[1] + self.velocidad * sin(self.orientacion))
                else:
                    self.position = (self.position[0], 0)


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Juego de Felipe')
        self.personaje = Personaje(self, 130, 40)
        self.setGeometry(500, 500, 600, 600)
        self.show()
        self.center()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.personaje.velocidad = 3
            self.personaje.mover = True
        elif event.key() == Qt.Key_S:
            self.personaje.velocidad = -3
            self.personaje.mover = True
        elif event.key() == Qt.Key_D:
            self.personaje.velocidad_giro = pi/20
        elif event.key() == Qt.Key_A:
            self.personaje.velocidad_giro = -pi/20


    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_W:
            self.personaje.mover = False
        elif event.key() == Qt.Key_S:
            self.personaje.mover = False
        elif event.key() == Qt.Key_D:
            self.personaje.velocidad_giro = 0
        elif event.key() == Qt.Key_A:
            #self.personaje.girar = True
            self.personaje.velocidad_giro = 0

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    @staticmethod
    def actualizar_imagen(myImageEvent):
        # Recibo el objeto con la información necesaria para mover a bastián
        # Hagamos un print para corroborar su posición?
        print(myImageEvent.x, myImageEvent.y)
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)


if __name__ == '__main__':
    app = QApplication([])
    ex = Ventana()
    ex.personaje.start()  # Ojo con esto, no empiecen el thread antes de empezar nuestro thread principal!
    sys.exit(app.exec_())
