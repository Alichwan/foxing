from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsEllipseItem, QProgressBar, QLabel, QGraphicsTextItem
from PyQt5.QtMultimedia import QSound
from math import hypot, degrees, atan2, cos, sin, radians, floor
from random import triangular, expovariate, randint, random, choice


def enemy_spawn(qtimer, lista_enemigos, level, scene, parent):
	if len(lista_enemigos) > 14 - level:
		qtimer.setInterval(expovariate(Entity.enemy_apparition_stats[level][0]) * 1000)
	else:
		enemigo = Enemy("assets/Enemy/Full Health/Enemy_Health_{0}.png", "Enemy", level, parent)
		lista_enemigos.append(enemigo)
		qtimer.setInterval(expovariate(Entity.enemy_apparition_stats[level][0]) * 1000)
		enemigo.setPos(randint(0, 800), randint(0, 500))
		scene.addItem(enemigo)


def rect2pol(x, y):
	norma = hypot(x, y)
	angulo = (degrees(atan2(y, x)) + 90) % 360
	return norma, angulo


def pol2rect(radio, theta):
	theta = radians((theta - 90))
	x = radio * cos(theta)
	y = radio * sin(theta)
	return x, y


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


class Entity_Dies:
	def __init__(self, entity, type):
		self.entity = entity
		self.type = type


class aux_signal_emiter(QObject):
	trigger = pyqtSignal(Entity_Dies)

	def __init__(self, parent):
		super().__init__()
		self.trigger.connect(parent.eliminate_entity)
		pass

	def signal_sender(self, object, type):
		self.trigger.emit(Entity_Dies(object, type))


class Entity(QGraphicsPixmapItem):
	trigger = pyqtSignal(Entity_Dies)

	nivel = 0
	enemy_apparition_stats = [(1 / 10, 1, 5, 1), (1 / 8, 1, 6, 3), (1 / 6, 3, 7, 5), (1 / 4, 5, 9, 7),
	                          (1 / 2, 7, 10, 9)]

	def __init__(self, type, level, parent):  # type puede ser enemigo o jugador

		super().__init__()

		self.orientation = 0
		self.angular_velocity = 0
		self.velocity = 0
		self.setTransformOriginPoint(50, 50)

		self.aux_signal_object = aux_signal_emiter(parent)

		self.type = type
		self.level = level
		self.set_atrributes()
		self.set_health()
		self.wall = QSound("sounds/effects/wall.wav", parent=None)
		self.wall.setLoops(1)

	def set_atrributes(self):
		if self.type == "Enemy":
			self.datos = Entity.enemy_apparition_stats[self.level]
			self.tamaño = floor(triangular(self.datos[1], self.datos[2], self.datos[3]))
			self.ponderador = self.tamaño / 10
			pass
		else:
			self.tamaño = 2
			self.ponderador = 0.2

	def set_health(self):
		self.max_health = 20 * self.tamaño + 100
		self.health = 20 * self.tamaño + 100


class Enemy(Entity):
	contador_enemigos = 1

	def __init__(self, dir_assets, *args):
		super().__init__(*args)

		self.name = "Enemigo {0}".format(Enemy.contador_enemigos)
		self.sprite_generator = sprite_generator(dir_assets, 12, 13)
		next(self.sprite_generator)

		self.set_health_var()
		self.set_pixmap_image()
		self.set_animation_timer()
		self.velocity = 5
		self.orientation = 0
		self.angular_velocity = 0
		self.player_in_range = False
		self.aux_aux_move = True

		self.atacar = True
		self.set_attack_timer()

		self.attack_velocity = 1000

		self.setTransformOriginPoint(50 * self.ponderador, 50 * self.ponderador)
		self.size_radius = QGraphicsEllipseItem(3 * self.ponderador, 3 * self.ponderador, self.tamaño * 12,
		                                        self.tamaño * 12, parent=self)
		self.vision_radius = QGraphicsEllipseItem(-86 * self.ponderador, -86 * self.ponderador, self.tamaño * 30,
		                                          self.tamaño * 30, parent=self)
		self.escape_radius = QGraphicsEllipseItem(-160 * self.ponderador, -160 * self.ponderador, self.tamaño * 45,
		                                          self.tamaño * 45, parent=self)

		self.set_movement_timer()

	def set_attack_timer(self):
		self.attack_timer = QTimer()
		self.attack_timer.timeout.connect(self.reset_attack)

	def reset_attack(self):
		self.atacar = True
		self.attack_timer.stop()

	def set_pixmap_image(self):  # descriptivo
		self.pixmap_image = QPixmap(next(self.sprite_generator)).scaled(self.ponderador * 128, self.ponderador * 128)
		self.setTransformOriginPoint(50 * self.ponderador, 50 * self.ponderador)
		self.setPixmap(self.pixmap_image)
		self.health_var.update(self.health)

	def set_animation_timer(
			self):  # timer para que se actualize el sprite periodicamente, ya que es un dragon y los dragones vuelan :D
		self.animation_timer = QTimer()
		self.animation_timer.timeout.connect(self.set_pixmap_image)
		self.animation_timer.start(85)

	def set_health_var(self):
		self.health_var = Health_Bar(self.max_health, 200 * self.ponderador)
		self.health_var.setParentItem(self)
		self.health_var.setX(-60 * self.ponderador)
		self.health_var.setTransformOriginPoint(118.76 * self.ponderador, 58.76 * self.ponderador)
		self.health_var.show()

	def choice(self):
		if random() < 0.25:
			self.aux_move = True
			self.aux_aux_move = True
		else:
			self.aux_move = False

	def set_movement_timer(self):
		self.aux_move = choice([True, False])

		self.still_moving = QTimer()
		self.still_moving.start(1000)
		self.still_moving.timeout.connect(self.choice)

		self.movement_timer = QTimer()
		self.movement_timer.timeout.connect(self.movement)
		self.movement_timer.start(50)

	def movement(self):
		object_list = self.vision_radius
		if not self.player_in_range:
			if self.aux_move:
				if self.aux_aux_move:
					self.orientation = randint(0, 360)
					self.setRotation(self.orientation)
					self.health_var.setRotation(-self.orientation)
					self.aux_aux_move = False
				self.collide_with_items()
				self.move()
			else:
				self.collide_with_items()
				self.move()

		elif self.player_in_range:
			self.move()

	def move(self):
		if self.move:
			self.change_in_x, self.change_in_y = pol2rect(self.velocity, self.orientation)
			if self.x() + self.change_in_x < 0 or self.x() + self.change_in_x + 64 * self.ponderador > 900:
				if self.y() + self.change_in_y < 0 or self.y() + self.change_in_y + 64 * self.ponderador > 600:
					pass
				else:
					self.setPos(self.x(), self.y() + self.change_in_y)
					pass
			elif self.y() + self.change_in_y < 0 or self.y() + self.change_in_y + 64 * self.ponderador > 600:
				if self.x() + self.change_in_x < 0 or self.x() + self.change_in_x + 64 * self.ponderador > 900:
					pass
				else:
					self.setPos(self.x() + self.change_in_x, self.y())
			else:
				self.setPos(self.x() + self.change_in_x, self.y() + self.change_in_y)

	def enemy_attack(self, enemy):
		self.damage = round(self.tamaño * 1 / 10 * self.max_health, 0)
		enemy.health_var.update(self.damage)
		enemy.health -= self.damage
		self.atacar = False
		self.attack_timer.start(self.attack_velocity)
		if enemy.health < 0:
			self.aux_signal_object.signal_sender(enemy, "Player")

	def collide_with_items(self):
		self.object_list = self.collidingItems()
		for object in self.object_list:
			if isinstance(object, Enemy) or isinstance(object, Main_Player) and self.move:
				self.change_in_x, self.change_in_y = pol2rect(6, self.orientation)
				if self.velocity > 0:
					self.setPos(self.x() - self.change_in_x, self.y() - self.change_in_y)
					if isinstance(object, Main_Player) and self.atacar:
						self.enemy_attack(object)
				else:
					self.setPos(self.x() + self.change_in_x, self.y() + self.change_in_y)
					self.enemy_attack(object)


class Main_Player(Entity):
	contador = 1

	def __init__(self, dir_assets, *args):
		super().__init__(*args)

		self.name = "Jugador {0}".format(Main_Player.contador)
		self.sprite_generator = sprite_generator(dir_assets, 7, 8)
		next(self.sprite_generator)
		self.experience = 0
		self.progress_bar = Progress_Bar(1000)

		self.set_health_var()
		self.set_pixmap_image()
		self.set_attack_timer()
		self.set_animation_timer()

		self.attack_velocity = 1000
		self.move = True
		self.atacar = True
		self.level_impar = False

		self.set_movement_timer()
		self.setTransformOriginPoint(50 * self.ponderador, 50 * self.ponderador)
		self.score = 0
		self.set_score_timer()

		self.score_label = QGraphicsTextItem()
		self.score_label.setDefaultTextColor(QColor("green"))

		Main_Player.contador += 1

	def set_score_timer(self):
		self.score_timer = QTimer()
		self.score_timer.timeout.connect(self.add_score)
		self.score_timer.start(1000)

	def add_score(self):
		self.score += 50
		self.score_label.setHtml(
			'<div style="background:white;">{0} Score: '.format(self.name) + str(self.score) + '</p>')

	def set_experience(self, experience):
		self.experience += experience
		print(self.experience)
		level_up = self.progress_bar.set_actual_experience(experience)
		if level_up and not self.level_impar:
			self.tamaño += 1
			self.level_impar = True
			for i in range(0, 100):
				self.ponderador += 0.001
				print(self.ponderador)

	def set_attack_timer(self):
		self.attack_timer = QTimer()
		self.attack_timer.timeout.connect(self.reset_attack)

	def reset_attack(self):
		self.atacar = True
		self.attack_timer.stop()

	def set_movement_timer(self):

		self.movement_timer = QTimer()
		self.movement_timer.timeout.connect(self.movement)
		self.movement_timer.start(50)

	def movement(self):
		self.orientation += self.angular_velocity
		self.setRotation(self.orientation)
		self.health_var.setRotation(-self.orientation)
		self.collide_with_items()
		if self.move:
			self.change_in_x, self.change_in_y = pol2rect(self.velocity, self.orientation)
			if self.x() + self.change_in_x < 0 or self.x() + self.change_in_x + 64 * self.ponderador > 900:
				if self.y() + self.change_in_y < 0 or self.y() + self.change_in_y + 64 * self.ponderador > 600:
					self.wall.play()
				else:
					self.setPos(self.x(), self.y() + self.change_in_y)
					self.wall.play()
			elif self.y() + self.change_in_y < 0 or self.y() + self.change_in_y + 64 * self.ponderador > 600:
				if self.x() + self.change_in_x < 0 or self.x() + self.change_in_x + 64 * self.ponderador > 900:
					self.wall.play()
				else:
					self.setPos(self.x() + self.change_in_x, self.y())
					self.wall.play()
			else:
				self.setPos(self.x() + self.change_in_x, self.y() + self.change_in_y)

	def resize_health_bar(self):
		self.health_var.setScale(self.tamaño * self.ponderador)

	def set_pixmap_image(self):  # descriptivo
		self.pixmap_image = QPixmap(next(self.sprite_generator)).scaled(self.ponderador * 128, self.ponderador * 128)
		self.setTransformOriginPoint(50 * self.ponderador, 50 * self.ponderador)
		self.setPixmap(self.pixmap_image)
		self.health_var.update(self.health)
		self.progress_bar.fill()
		self.resize_health_bar()

	def set_animation_timer(
			self):  # timer para que se actualize el sprite periodicamente, ya que es un dragon y los dragones vuelan :D
		self.animation_timer = QTimer()
		self.animation_timer.timeout.connect(self.set_pixmap_image)
		self.animation_timer.start(85)

	def set_health_var(self):
		self.health_var = Health_Bar(self.max_health, 200 * self.ponderador)
		self.health_var.setParentItem(self)
		self.health_var.setX(-60 * self.ponderador)
		self.health_var.setTransformationMode(Qt.SmoothTransformation)
		self.health_var.setTransformOriginPoint(118.76 * self.ponderador, 58.76 * self.ponderador)

	def enemy_attack(self, enemy):
		self.damage = round(self.tamaño * 1 / 10 * self.max_health, 0)
		enemy.health -= self.damage
		enemy.health_var.update(enemy.health)
		self.atacar = False
		self.attack_timer.start(self.attack_velocity)
		if enemy.health < 0:
			if self.health > 0:
				self.set_experience(100 * max(enemy.tamaño - self.tamaño + 3, 1))
				self.score += 1000 * abs((enemy.tamaño - self.tamaño))
			self.aux_signal_object.signal_sender(enemy, "Enemy")

	def collide_with_items(self):
		self.object_list = self.collidingItems()
		for object in self.object_list:
			if isinstance(object, Enemy) or isinstance(object, Main_Player) and self.move:
				self.change_in_x, self.change_in_y = pol2rect(6, self.orientation)
				if self.velocity > 0:
					self.setPos(self.x() - self.change_in_x, self.y() - self.change_in_y)
					if isinstance(object, Enemy) and self.atacar:
						self.enemy_attack(object)
				else:
					self.setPos(self.x() + self.change_in_x, self.y() + self.change_in_y)


class Health_Bar(QGraphicsPixmapItem):
	def __init__(self, vida_max, largo):
		super().__init__()
		self.vida_max = vida_max
		self.largo = largo
		self.marco = QGraphicsPixmapItem(QPixmap("assets/vida/relleno.png").scaled(largo, 5), parent=self)

	def update(self, vida):
		self.marco.setPixmap(QPixmap("assets/vida/relleno.png").scaled(self.largo * (vida / self.vida_max), 5))


class Progress_Bar(QProgressBar):
	def __init__(self, experiencia_maxima):
		super().__init__()
		self.experiencia_maxima = experiencia_maxima
		self.setGeometry(30, 40, 200, 25)
		self.experiencia_actual = 0
		self.step = 0

	def set_actual_experience(self, experiencia):
		self.experiencia_actual += experiencia
		if self.experiencia_actual >= 500:
			return (True)
		return False

	def fill(self):
		if self.step > 100:
			return True
		elif self.experiencia_actual * 100 / self.experiencia_maxima > self.step:
			print(self.step)
			self.step += 0.5
			self.setValue(self.step)
			return False
