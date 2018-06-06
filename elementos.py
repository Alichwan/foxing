from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from random import uniform, choice, randint
from player import Enemy, pol2rect, Main_Player


def object_spawn(qtimer, lista_objetos, scene, parent):
	if len(lista_objetos) > 14:
		qtimer.setInterval(uniform(1, 30) * 1000)
	else:
		eleccion = choice(["bomba", "vida", "moneda", "safe_zone"])
		if eleccion == "bomba":
			objeto = Bomb(parent)
		elif eleccion == "vida":
			objeto = Vida(parent)
		elif eleccion == "moneda":
			objeto = Coin(parent)
		else:
			objeto = SafeZone()
		lista_objetos.append(objeto)
		qtimer.setInterval(uniform(1, 30) * 1000)
		objeto.setPos(randint(0, 800), randint(0, 500))
		scene.addItem(objeto)


def sprite_generator(main_string, num, num_imagenes):
	"""genera el sprite para simular el movimiento, recibe la cantidad
	de elementos - 1 sprites disponibles para simular el movimiento.
	retorna el siguiente en la cadena para generar el movimiento"""

	aux_sprite_list = sprite_list(main_string, num_imagenes)
	n = 0
	yield (None)
	while n > -1:
		yield (aux_sprite_list[n])
		if n == num:
			n = 0
		else:
			n += 1


def sprite_list(main_string, n):
	"""recibe la direccion en donde se encuentra el sprite
	(todos con un nombre generico) diferenciado por un numero.
	esta funcion se encarga de asignar el numero"""

	return [main_string.format(num) for num in range(n)]


class ObjectDies:
	def __init__(self, object, entity, type):
		self.object = object
		self.entity = entity
		self.type = type


class aux_signal_emiter(QObject):
	trigger = pyqtSignal(ObjectDies)

	def __init__(self, parent):
		super().__init__()
		self.trigger.connect(parent.eliminate_object)

	def signal_sender(self, object, entity, type):
		self.trigger.emit(ObjectDies(object, entity, type))


class Bomb(QGraphicsPixmapItem):
	def __init__(self, parent):
		super().__init__()
		self.bomb = sprite_generator("assets/items/Bomb/Bomb/bomba_{0}.png", 2, 3)
		next(self.bomb)
		self.explosion = sprite_generator("assets/items/Bomb/Explosion/explosion_{0}.png", 15, 16)
		next(self.explosion)
		self.bomb_radius = QGraphicsEllipseItem(0, 0, 60, 60, parent=self)
		self.set_animation_timer()
		self.activada = False
		self.aux_signal_object = aux_signal_emiter(parent)

	def set_animation_timer(self):
		self.animation_timer = QTimer()
		self.animation_timer.timeout.connect(self.animation_movement)
		self.animation_timer.start(50)

	def animation_movement(self):
		self.colision_with()
		if not self.activada:
			self.pixmap_image = QPixmap(next(self.bomb))
			self.setPixmap(self.pixmap_image)
		elif self.activdad:
			pass

	def colision_with(self):
		self.lista_objetos = self.collidingItems()
		for elemento in self.lista_objetos:
			if isinstance(elemento, Main_Player):
				self.aux_signal_object.signal_sender(self, elemento, "bomba")


class Coin(QGraphicsPixmapItem):
	def __init__(self, parent):
		super().__init__()
		self.sprite_generator = sprite_generator("assets/items/Coins/coin_{0}.png", 24, 25)
		next(self.sprite_generator)
		self.set_animation_timer()
		self.aux_signal_object = aux_signal_emiter(parent)

	def set_animation_timer(self):
		self.animation_timer = QTimer()
		self.animation_timer.timeout.connect(self.animation_movement)
		self.animation_timer.start(40)

	def animation_movement(self):
		self.pixmap_image = QPixmap(next(self.sprite_generator)).scaled(45, 45)
		self.setPixmap(self.pixmap_image)
		self.colision_with()

	def colision_with(self):
		self.lista_objetos = self.collidingItems()
		for elemento in self.lista_objetos:
			if isinstance(elemento, Main_Player):
				self.aux_signal_object.signal_sender(self, elemento, "moneda")


class SafeZone(QGraphicsPixmapItem):
	def __init__(self):
		super().__init__()
		self.setPixmap(QPixmap("assets/items/Safe Zone/safe_zone.png"))
		self.set_colision_timer()

	def set_colision_timer(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.colision_with)
		self.timer.start(30)

	def colision_with(self):
		self.lista_objetos = self.collidingItems()
		for elemento in self.lista_objetos:
			if isinstance(elemento, Enemy):
				elemento.change_in_x, elemento.change_in_y = pol2rect(6, elemento.orientation)
				if elemento.velocity > 0:
					elemento.setPos(elemento.x() - elemento.change_in_x, elemento.y() - elemento.change_in_y)
				else:
					elemento.setPos(elemento.x() + elemento.change_in_x, elemento.y() + elemento.change_in_y)


class Vida(QGraphicsPixmapItem):
	def __init__(self, parent):
		super().__init__()
		self.setPixmap(QPixmap("assets/items/Heart/vida_extra.png").scaled(30, 30))
		self.aux_signal_object = aux_signal_emiter(parent)
		self.set_colision_timer()

	def set_colision_timer(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.colision_with)
		self.timer.start(30)

	def colision_with(self):
		self.lista_objetos = self.collidingItems()
		for elemento in self.lista_objetos:
			if isinstance(elemento, Main_Player):
				self.aux_signal_object.signal_sender(self, elemento, "vida")
