import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):
        self.setGeometry(300, 100, 225, 450)
        self.setMaximumHeight(450)
        self.setMaximumWidth(225)
        self.setWindowTitle('Move Event')

        self.blue_hide = True
        self.blue_label = QLabel('AZUL', self)
        self.blue_label.move(0, 0)
        self.blue_label.setGeometry(QRect(0, 0, 225, 225))  # (x, y, height, width)
        self.pixmap_azul = QPixmap('images/colors/azul.png')
        self.blue_label.setPixmap(self.pixmap_azul)
        self.blue_label.show()

        self.green_hide = True
        self.green_label = QLabel('VERDE', self)
        self.green_label.move(0, 0)
        self.green_label.setGeometry(QRect(0, 225, 225, 225))
        self.pixmap_verde = QPixmap('images/colors/verde.png')
        self.green_label.setPixmap(self.pixmap_verde)
        self.green_label.show()

        self.show()

    def mousePressEvent(self, event):
        if event.y() <= 225:  # Este es el alto del label
            if self.blue_hide:
                self.blue_label.hide()
            else:
                self.blue_label.show()
            self.blue_hide = not self.blue_hide
        else:
            if self.green_hide:
                self.green_label.hide()
            else:
                self.green_label.show()
            self.green_hide = not self.green_hide


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())