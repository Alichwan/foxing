import sys
from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, QPalette, QFont, QColor
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, QCoreApplication, QUrl
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, \
	QLineEdit, QGridLayout, QDesktopWidget, QToolTip, QGraphicsScene, QGraphicsView, QFileDialog, \
	QMessageBox
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaPlaylist, QMediaContent
from player import Main_Player, enemy_spawn
from random import randint
from elementos import object_spawn


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.two_player = False

		self.main_window_objects = []  # para mantener los Qwidgets almacenados
		self.highscore_objects = []
		self.set_main_background()

		self.setup_main_music()
		self.setup_labels()
		self.__setUp()
		self.setFocusPolicy(Qt.StrongFocus)

		self.enemy_list = []
		self.object_list = []
		self.level = 1

	def __setUp(self):
		self.create_main_window()
		self.main_window_buttons()
		self.setup_main_window_music()
		self.create_highscore_window()
		self.hide_highscore_window()
		self.hide_highscore_window()
		self.show()

	def button_click(self):
		self.music_dict["Click"].play()

	def set_main_background(self):
		palette = QPalette()
		pixmap = QPixmap("assets/backgrounds/main_background.jpg").scaled(800, 450)
		brush = QBrush(pixmap)
		palette.setBrush(QPalette.Background, brush)
		self.setPalette(palette)

	def setup_main_music(self):
		self.music_dict = dict()
		self.music_dict["Main Title"] = QSound("sounds/Main.wav", parent=None)
		self.music_dict["Top 10"] = QSound("sounds/Top10.wav", parent=None)
		self.music_dict["Main Title"].setLoops(-1)
		self.music_dict["Top 10"].setLoops(-1)
		self.music_dict["Click"] = QSound("sounds/effects/button click.wav", parent=None)
		self.music_dict["Click"].setLoops(1)
		self.music_dict["Enemy Die"] = QSound("sounds/effects/enemy_die.wav", parent=None)
		self.music_dict["Enemy Die"].setLoops(1)

	def setup_labels(self):
		self.label_dict = dict()
		self.main_logo = QPixmap("assets/dccellsv3.png")
		self.highscore_logo = QPixmap("assets/highscoresv2.png")
		self.label_dict["main logo"] = QLabel("")
		self.label_dict["main logo"].setPixmap(self.main_logo)
		self.label_dict["highscores logo"] = QLabel("")
		self.label_dict["highscores logo"].setPixmap(self.highscore_logo)

	def create_main_window(self):
		self.resize(800, 450)
		self.center_window()
		self.setWindowTitle('DCCells (not another agar.io game)')  # set window title
		self.setWindowIcon(QIcon('assets/mini_logo.png'))  # allows setting window icon

		self.mainvbox = QVBoxLayout(self)
		self.button_layout = QVBoxLayout(self)

		self.imagebox = QHBoxLayout(self)
		self.imagebox.addWidget(self.label_dict["main logo"])
		self.imagebox.setAlignment(Qt.AlignCenter)

		self.mainvbox.addLayout(self.imagebox)

	def center_window(self):
		reference_frame = self.frameGeometry()
		center_point = QDesktopWidget().availableGeometry().center()
		reference_frame.moveCenter(center_point)
		self.move(reference_frame.topLeft())

	def main_window_buttons(self):
		self.playdccsells = QPushButton("Jugar DCCells", self)
		self.playdccsells.setToolTip('Iniciar DCCells, una aventura epica')
		self.playdccsells.clicked.connect(self.change_game_window)
		self.playdccsells.resize(self.playdccsells.sizeHint())
		self.playdccsells.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')
		self.main_window_objects.append(self.playdccsells)

		self.openhighscore = QPushButton("Mejores Jugadores", self)
		self.openhighscore.setToolTip('Revisa a las leyendas a superar')
		self.openhighscore.clicked.connect(self.change_score_window)
		self.openhighscore.resize(self.openhighscore.sizeHint())
		self.openhighscore.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')
		self.main_window_objects.append(self.openhighscore)

		self.exitdccels = QPushButton("Salir", self)
		self.exitdccels.setToolTip('Salir de esta aventura epica')
		self.exitdccels.resize(self.exitdccels.sizeHint())
		self.exitdccels.clicked.connect(self.exit_dccells)
		self.exitdccels.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')
		self.main_window_objects.append(self.exitdccels)

		self.selectmusicfolder = QPushButton("Elegir Musica", self)
		self.selectmusicfolder.setToolTip('Busca tu carpeta de musica preferida para escuchar mientras juegas')
		self.selectmusicfolder.resize(self.selectmusicfolder.sizeHint())
		self.selectmusicfolder.clicked.connect(self.set_own_music)
		self.selectmusicfolder.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')
		self.main_window_objects.append(self.selectmusicfolder)

		self.two_player_button = QPushButton("Activar 2 Jugadores", self)
		self.two_player_button.setToolTip('Unete en una epica campaña con tu camarada')
		self.two_player_button.clicked.connect(self.add_second_player)
		self.two_player_button.resize(self.playdccsells.sizeHint())
		self.two_player_button.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')
		self.main_window_objects.append(self.two_player_button)

		self.zero_row = QHBoxLayout(self)
		self.zero_row.addWidget(self.two_player_button)
		self.zero_row.setAlignment(Qt.AlignRight)

		self.first_row = QHBoxLayout(self)
		self.first_row.addWidget(self.playdccsells)
		self.first_row.addWidget(self.openhighscore)

		self.second_row = QHBoxLayout(self)
		self.second_row.addWidget(self.selectmusicfolder)
		self.second_row.addWidget(self.exitdccels)

		self.button_layout.addLayout(self.first_row)
		self.button_layout.addLayout(self.second_row)
		self.button_layout.setAlignment(Qt.AlignBottom)
		self.mainvbox.addLayout(self.zero_row)
		self.mainvbox.addLayout(self.button_layout)
		self.mainvbox.setSpacing(12.5)

	def add_second_player(self):
		if not self.two_player:
			self.two_player = True
			self.two_player_button.setText("Desactivar 2 Jugadores")
			self.two_player_button.setToolTip("Vuelve a tu solitaria cruzada por dominar el mundo")
		else:
			self.two_player = False
			self.two_player_button.setText("Activar 2 Jugadores")
			self.two_player_button.setToolTip('Unete en una epica campaña con tu camarada')

	def setup_main_window_music(self):
		self.music_dict["Top 10"].stop()
		self.music_dict["Main Title"].play()

	def exit_dccells(self):
		self.button_click()
		QCoreApplication.instance().quit()

	def change_score_window(self):
		self.button_click()
		self.set_highscore_background()
		self.setup_highscore_music()
		self.resize(300, 650)
		self.center_window()
		self.setWindowTitle('DCCells (not another agar.io game) Highscores')  # set window title
		self.highscore_buttom.show()
		self.label_dict["highscores logo"].show()
		self.hide_main_window()

	def set_highscore_background(self):
		palette = QPalette()
		pixmap = QPixmap("assets/backgrounds/Highscorebackground.jpeg").scaled(750, 700)
		brush = QBrush(pixmap)
		palette.setBrush(QPalette.Background, brush)
		self.setPalette(palette)

	def hide_main_window(self):
		for button in self.main_window_objects: button.hide()
		self.label_dict["main logo"].hide()

	def hide_highscore_window(self):
		self.label_dict["highscores logo"].hide()
		self.highscore_buttom.hide()

	def change_main_window(self):
		self.button_click()
		self.hide_highscore_window()
		self.setup_main_window_music()
		self.resize(800, 450)
		self.center_window()
		self.setWindowTitle('DCCells (not another agar.io game)')  # set window title
		for button in self.main_window_objects: button.show()
		self.label_dict["main logo"].show()
		self.set_main_background()

	def create_highscore_window(self):

		self.highscore_vbox = QVBoxLayout(self)
		self.button_layout = QHBoxLayout(self)

		self.image_highscore_box = QHBoxLayout(self)
		self.image_highscore_box.addWidget(self.label_dict["highscores logo"])
		self.image_highscore_box.setAlignment(Qt.AlignTop)

		self.highscore_buttom = QPushButton("Volver")
		self.highscore_buttom.setToolTip('Volver a la pantalla principal')
		self.highscore_buttom.resize(self.highscore_buttom.sizeHint())
		self.highscore_buttom.clicked.connect(self.change_main_window)
		self.highscore_buttom.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')

		self.highscore_hbox = QHBoxLayout(self)
		self.highscore_hbox.addWidget(self.highscore_buttom)
		self.highscore_vbox.addLayout(self.image_highscore_box)
		self.highscore_vbox.addLayout(self.highscore_hbox)
		self.mainvbox.addLayout(self.highscore_vbox)

	def setup_highscore_music(self):
		self.music_dict["Main Title"].stop()
		self.music_dict["Top 10"].play()

	def hide_game_window(self):
		self.scene_viewer.hide()

	def enemy_aux_function(self):
		enemy_spawn(self.enemy_timer, self.enemy_list, self.level, self.scene, self)

	def set_enemy_timer(self):
		self.enemy_timer = QTimer()
		self.enemy_timer.timeout.connect(self.enemy_aux_function)
		self.enemy_timer.start(1)

	def object_aux_function(self):
		object_spawn(self.objec_timer, self.object_list, self.scene, self)

	def set_object_timer(self):
		self.objec_timer = QTimer()
		self.objec_timer.timeout.connect(self.object_aux_function)
		self.objec_timer.start(1)

	def set_game_window(self):

		self.scene = QGraphicsScene()
		self.button_n_progresshbox = QHBoxLayout()
		self.game_items = []

		# añadiendo primer jugador
		self.main_player = Main_Player("assets/Main_player/full_health/health_{0}.png", "player", 1, self)
		self.main_player.setPos(randint(0, 800), randint(0, 500))
		self.scene.addItem(self.main_player)
		self.scene.addItem(self.main_player.score_label)
		self.button_n_progresshbox.addWidget(self.main_player.progress_bar)
		# añadiendo_segundo_jugador
		if self.two_player:
			self.second_player = Main_Player("assets/Main_player/mid_health/mid_health{0}.png", "player", 1, self)
			self.second_player.setPos(randint(0, 800), randint(0, 500))
			self.scene.addItem(self.second_player)
			self.scene.addItem(self.second_player.score_label)
			self.second_player.score_label.setPos(770, 0)
			self.button_n_progresshbox.addWidget(self.second_player.progress_bar)

		self.scene_viewer = QGraphicsView(self.scene, self)
		self.scene_viewer.setFixedSize(900, 600)
		self.scene.setSceneRect(0, 0, 900, 600)
		self.scene_viewer.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scene_viewer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.imagen = QImage("assets/backgrounds/game_background.jpg").scaled(900, 600)
		self.scene.setBackgroundBrush(QBrush(self.imagen))

		self.back_menu_buttom = QPushButton("Volver")
		self.back_menu_buttom.setToolTip('Volver a la pantalla principal')
		self.back_menu_buttom.resize(self.highscore_buttom.sizeHint())
		self.back_menu_buttom.clicked.connect(self.back_main_window)
		self.back_menu_buttom.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')
		self.button_n_progresshbox.addWidget(self.back_menu_buttom)

		self.game_hbox = QHBoxLayout()
		self.game_hbox.addWidget(self.scene_viewer)
		self.mainvbox.addLayout(self.game_hbox)
		self.mainvbox.addLayout(self.button_n_progresshbox)

		self.game_items.append(self.scene_viewer)
		self.game_items.append(self.button_n_progresshbox)

	def back_main_window(self):
		pass

	def change_game_window(self):
		self.resize(900, 700)
		self.center_window()
		self.hide_main_window()
		self.set_game_window()
		self.set_enemy_timer()
		self.set_object_timer()
		self.scene_viewer.show()

	def keyPressEvent(self, event):
		if event.isAutoRepeat():
			pass
		elif event.key() == Qt.Key_W:
			self.main_player.velocity = 5
			self.main_player.move = True
		elif event.key() == Qt.Key_S:
			self.main_player.move = True
			self.main_player.velocity = -5
		elif event.key() == Qt.Key_D:
			self.main_player.angular_velocity = 3
		elif event.key() == Qt.Key_A:
			self.main_player.angular_velocity = -3

		elif event.key() == Qt.Key_Up:
			if self.two_player:
				self.second_player.velocity = 5
				self.second_player.move = True
		elif event.key() == Qt.Key_Down:
			if self.two_player:
				self.second_player.move = True
				self.second_player.velocity = -5
		elif event.key() == Qt.Key_Right:
			if self.two_player:
				self.second_player.angular_velocity = 3
		elif event.key() == Qt.Key_Left:
			if self.two_player:
				self.second_player.angular_velocity = -3

	def keyReleaseEvent(self, event):
		if event.isAutoRepeat():
			pass
		elif event.key() == Qt.Key_W:
			self.main_player.move = False
		elif event.key() == Qt.Key_S:
			self.main_player.move = False
		elif event.key() == Qt.Key_D:
			self.main_player.angular_velocity = 0
		elif event.key() == Qt.Key_A:
			self.main_player.angular_velocity = 0

		elif event.key() == Qt.Key_Up:
			if self.two_player:
				self.second_player.move = False
		elif event.key() == Qt.Key_Down:
			if self.two_player:
				self.second_player.move = False
		elif event.key() == Qt.Key_Left:
			if self.two_player:
				self.second_player.angular_velocity = 0
		elif event.key() == Qt.Key_Right:
			if self.two_player:
				self.second_player.angular_velocity = 0

	def set_own_music(self):
		music_file = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Music files (*.mp3 *.wav)")
		self.main_playlist = QMediaPlaylist()
		path = QUrl.fromLocalFile(music_file[0])
		self.main_playlist.addMedia(QMediaContent(path))
		self.main_playlist.setPlaybackMode(QMediaPlaylist.Loop)
		self.music_player = QMediaPlayer()
		self.music_player.setPlaylist(self.main_playlist)
		self.music_dict["Main Title"].stop()
		self.music_player.play()

	def game_over(self):
		print("se acabo el juego")
		self.dialogo = QWidget()
		QMessageBox.about(self.dialogo, "Eres un perdedor", "Has perdido :( !! Intenta todo nuevamente")
		self.back_main_window()

	def eliminate_entity(self, entity_event):
		if entity_event.type == "Player":
			self.game_over()
		else:
			enemigo = self.enemy_list[self.enemy_list.index(entity_event.entity)]
			self.scene.removeItem(enemigo)
			self.enemy_list.remove(enemigo)
			self.music_dict["Enemy Die"].play()
			del (entity_event.entity)

	def add_coin_score(self, object_event):
		object_event.entity.score += 1000
		self.scene.removeItem(object_event.object)
		self.object_list.remove(object_event.object)
		del (object_event.object)

	def add_health(self, object_event):
		object_event.entity.health = object_event.entity.max_health
		self.scene.removeItem(object_event.object)
		self.object_list.remove(object_event.object)
		del (object_event.object)

	def eliminate_object(self, object_event):
		if object_event.type == "moneda":
			self.add_coin_score(object_event)
		elif object_event.type == "bomba":
			print("bomba")
		elif object_event.type == "vida":
			self.add_health(object_event)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	main_game = MainWindow()
	sys.exit(app.exec_())
