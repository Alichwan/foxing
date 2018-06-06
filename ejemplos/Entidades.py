from PyQt5.QtWidgets import QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QApplication, QVBoxLayout,\
    QGraphicsEllipseItem, QPushButton, QLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap

from Extras import BarraVida

import math
import time

# -------------------------------------------------------------------------------


class Player(QGraphicsPixmapItem):

    def __init__(self, champ):
        super().__init__()
        self.setPos(200, 250)

        # Valores Utiles despues
        self.angulo = 0
        self.mouse = (0, 0)
        self.equipo = 1
        self.nombre = champ
        self.target = None
        self.muerto = False
        self.muertes = 0

        # Stats
        if champ == "Chau":
            self.setPixmap(QPixmap("Player/Chau/player_0.png").scaled(50, 50))

            paths = ["player_{}".format(i) for i in range(8)]
            paths = sorted([p for i in range(3) for p in paths])

            self.vida = 500
            self.rango = 40
            self.velocidad = 30
            self.v_atk = 10
            self.daño = 5

        elif champ == "Hernan":
            self.setPixmap(QPixmap("Player/Hernan/peludo0.png").scaled(50, 50))
            paths = ["peludo{}".format(i) for i in range(16)]
            paths = sorted([p for i in range(3) for p in paths])

            self.vida = 666
            self.rango = 5
            self.velocidad = 10
            self.v_atk = 10
            self.daño = 20

        elif champ == "Roberto":
            self.setPixmap(QPixmap("Player/Roberto/player0.png").scaled(50, 50))
            paths = ["player1", "player2", "player3", "player4", "player5", "player0"]
            paths = sorted([p for i in range(5) for p in paths])

            self.vida = 200
            self.rango = 70
            self.velocidad = 15
            self.v_atk = 20
            self.daño = 10

        # El generador de paths
        self.img = self.gen_path(paths)

        self.setTransformOriginPoint(25, 25)

        # Area de ataque
        self.area = QGraphicsEllipseItem(-self.rango, -self.rango, 50 + self.rango * 2, 50 + self.rango * 2)
        self.area.setParentItem(self)
        self.area.hide()

        # La barra de vida
        self.barra_vida = BarraVida(50, self.vida)
        self.barra_vida.setParentItem(self)

        # Se crean los timers de movimiento y ataque
        self.avanzar = QtCore.QTimer()
        self.avanzar.timeout.connect(self.acercarse)
        self.atacar = QtCore.QTimer()
        self.atacar.timeout.connect(self.ataque)

        #self.time = time.time()

    def gen_path(self, lista):
        while True:
            for path in lista:
                yield "Player/{}/{}.png".format(self.nombre, path)

    def mover(self, evento):
        # Apretar una tecla de movimiento cancela el movimiento automático
        self.avanzar.stop()
        self.atacar.stop()
        self.target = None
        #print(abs(self.time - time.time()))
        #self.time = time.time()

        text = evento.text()  # para no tener que escribirlo mil veces
        # se calcula un angulo en base a la ultima posicion del mouse
        x = self.x() + 25 - self.mouse[0]
        y = self.y() + 25 - self.mouse[1]
        self.angulo = - math.degrees(math.atan2(x, y))
        if self.angulo < 0:
            self.angulo += 360
        self.rotacion(self.angulo)

        # Cambia la imagen de movimiento
        self.setPixmap(QPixmap(next(self.img)).scaled(50, 50))

        if text == "w":
            self.setPos(self.x() + self.velocidad / 33.3 * math.sin(math.radians(180 - self.angulo)), self.y() + self.velocidad / 33.3 * math.cos(math.radians(180 - self.angulo)))

        elif text == "s":
            self.setPos(self.x() - self.velocidad / 33.3 * math.sin(math.radians(180 - self.angulo)), self.y() - self.velocidad / 33.3 * math.cos(math.radians(180 - self.angulo)))

        elif text == "d":
            self.setPos(self.x() + self.velocidad / 33.3 * math.sin(math.radians(90 - self.angulo)), self.y() + self.velocidad / 33.3 * math.cos(math.radians(90 - self.angulo)))

        elif text == "a":
            self.setPos(self.x() - self.velocidad / 33.3 * math.sin(math.radians(90 - self.angulo)), self.y() - self.velocidad / 33.3 * math.cos(math.radians(90 - self.angulo)))

    def stop(self):
        if self.nombre == "Roberto":
            self.setPixmap(QPixmap("Player/Roberto/player0.png").scaled(50, 50))

        elif self.nombre == "Chau":
            self.setPixmap(QPixmap("Player/Chau/player_0.png").scaled(50, 50))

        else:
            self.setPixmap(QPixmap("Player/Hernan/peludo0.png").scaled(50, 50))

    def rotacion(self, angulo):
        self.setRotation(angulo)
        self.barra_vida.setRotation(-angulo)

    def atacar_enemigo(self, target):
        self.target = target

        if self.target not in self.area.collidingItems():
            self.avanzar.start(50)

        else:
            self.atacar.start(1000 / self.v_atk)

    def acercarse(self):
        x = self.x() + 25 - self.target.x()
        y = self.y() + 25 - self.target.y()
        self.angulo = - math.degrees(math.atan2(x, y))
        if self.angulo < 0:
            self.angulo += 360
        self.rotacion(self.angulo)

        # Cambia la imagen de movimiento
        self.setPixmap(QPixmap(next(self.img)).scaled(50, 50))

        # Avanza
        self.setPos(self.x() + 0.05 * self.velocidad * math.sin(math.radians(180 - self.angulo)),
                    self.y() + 0.05 * self.velocidad * math.cos(math.radians(180 - self.angulo)))

        # Si llega el timer se termina
        if self.target in self.area.collidingItems():
            self.avanzar.stop()
            # Y ataca
            self.atacar.start(1000 / self.v_atk)

    def ataque(self):
        if self.scene() and self.target in self.scene().items():
            self.target.recibir_daño(self.daño)

        else:
            self.target = None
            self.atacar.stop()

    def recibir_daño(self, daño):
        self.vida -= daño
        self.barra_vida.update(self.vida)

        if self.vida <= 0:
            self.__scene = self.scene()
            self.scene().removeItem(self)
            self.muerto = True
            self.muertes += 1

            self.revivir = QtCore.QTimer()
            self.revivir.setSingleShot(True)
            self.revivir.timeout.connect(self.respawn)
            self.revivir.start(((1.1)**self.muertes) * 10000)

    def respawn(self):
        self.vida = self.barra_vida.vida
        self.barra_vida.update(self.vida)
        self.__scene.addItem(self)
        self.setPos(200, 250)

    def mouseMoveEvent(self, evento):
        if self.target == None:
            x = self.x() + 25 - evento.x()
            y = self.y() + 25 - evento.y()
            self.angulo = - math.degrees(math.atan2(x, y))
            if self.angulo < 0:
                self.angulo += 360
            self.rotacion(self.angulo)

            self.mouse = (evento.x(), evento.y())

# -------------------------------------------------------------------------------


class Minion(QGraphicsPixmapItem):

    def __init__(self, equipo, tamaño="pequeño"):
        self.equipo = equipo
        self.tamaño = tamaño
        super().__init__()
        if tamaño == "pequeño":
            self.setPixmap(QPixmap("Minions/minion0.png").scaled(30, 30))
            self.setTransformOriginPoint(15, 15)
        else:
            self.setPixmap(QPixmap("Minions/minion0.png").scaled(40, 40))
            self.setTransformOriginPoint(20, 20)
        paths = ["minion{}".format(i) for i in range(0, 9)]
        paths = sorted([p for i in range(3) for p in paths])
        self.img = self.gen_path(paths)

        # Area de ataque
        if tamaño == "pequeño":
            self.area = QGraphicsEllipseItem(-5, -5, 40, 40)
            self.area.setTransformOriginPoint(20, 20)
        else:
            self.area = QGraphicsEllipseItem(-20, -20, 80, 80)
            self.area.setTransformOriginPoint(40, 40)
        self.area.setParentItem(self)
        self.area.hide()

        # La barra de vida
        if tamaño == "pequeño":
            self.barra_vida = BarraVida(30, 45)
        else:
            self.barra_vida = BarraVida(40, 60)
        self.barra_vida.setParentItem(self)

        # Para cuando ataquen
        self.target = None

        # Stats
        if self.tamaño == "pequeño":
            self.vida = 45
            self.daño = 2
            self.pix = 30
        else:
            self.vida = 60
            self.daño = 4
            self.pix = 40

        self.mover = QtCore.QTimer()
        self.mover.timeout.connect(self.move)
        # Se mueve una vez cada 50 milisegundos
        self.mover.start(50)

        # Timer de ataque
        self.ataque = QtCore.QTimer()
        self.ataque.timeout.connect(self.atacar)

        self.hover = False

    def move(self):
        img = next(self.img)
        if self.hover is False:
            self.setPixmap(QPixmap(img).scaled(self.pix, self.pix))
        else:
            self.setPixmap(QPixmap(img + "_hover").scaled(self.pix, self.pix))
        meta = self.mas_cercano(self.enemigos)

        x = self.x() + 10 - meta[0]
        y = self.y() + 10 - meta[1]

        self.angulo = - math.degrees(math.atan2(x, y))
        if self.angulo < 0:
            self.angulo += 360
        self.rotacion(self.angulo + 180)

        self.setPos(self.x() + 0.4 * math.sin(math.radians(180 - self.angulo)), self.y() + 0.4 * math.cos(math.radians(180 - self.angulo)))

        # Si hay enemigos en el area empieza a atacar
        if len([i for i in self.area.collidingItems() if "equipo" in i.__dict__ and i.equipo != self.equipo]) > 0:
            self.mover.stop()
            self.setPixmap(QPixmap("Minions/minion0.png").scaled(self.pix, self.pix))
            self.ataque.start(1000)

    def rotacion(self, angulo):
        self.setRotation(angulo)
        self.barra_vida.setRotation(-angulo)

    def mas_cercano(self, lista):
        items = [(i.x(), i.y()) for i in lista]
        distancias = [self.dist(i) for i in items]

        return items[distancias.index(min(distancias))]

    def dist(self, punto):
        distancia = math.sqrt((punto[0] - self.x())**2 + (punto[1] - self.y())**2)

        return distancia

    def gen_path(self, lista):
        while True:
            for path in lista:
                yield "Minions/{}".format(path)

    def atacar(self):
        if self.target is None:
            enemigos = [i for i in self.area.collidingItems() if "equipo" in i.__dict__ and i.equipo != self.equipo]
            if len(enemigos) > 0:
                self.target = enemigos[0]
                self.target.recibir_daño(self.daño)

        # Esto para eliminar un bug que dejaba como target a objetos que ya no estaban en la scene (porque habian muerto)
        elif self.target not in self.scene().items():
            self.target = None

        else:
            self.target.recibir_daño(self.daño)

        if self.scene() and len([i for i in self.area.collidingItems() if "equipo" in i.__dict__ and i.equipo != self.equipo]) == 0:
            self.target = None
            self.ataque.stop()
            self.move()
            self.mover.start(50)

    def recibir_daño(self, daño):
        self.vida -= daño
        self.barra_vida.update(self.vida)

        if self.vida <= 0 and self.scene():
            self.scene().removeItem(self)
            self.ataque.stop()
            self.mover.stop()
            self.target = None

    def hoverEntra(self, evento):
        # Solo los enemigos son atacables
        if self.equipo == 2:
            self.hover = True
            if self.ataque.isActive():
                self.setPixmap(QPixmap("Minions/minion0_hover.png").scaled(self.pix, self.pix))

    def hoverSale(self, evento):
        self.hover = False
        if self.ataque.isActive():
            self.setPixmap(QPixmap("Minions/minion0.png").scaled(self.pix, self.pix))

    @property
    def enemigos(self):
        if self.scene():
            return [i for i in self.scene().items() if "equipo" in i.__dict__ and i.equipo != self.equipo]
