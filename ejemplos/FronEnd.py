import sys
from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, \
	QLineEdit, QGridLayout, QDesktopWidget, QToolTip
from PyQt5.Qt import QTest
from time import sleep
from PyQt5.QtMultimedia import QSound


class MainWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.main_window_objects = []  # para mantener los Qwidgets almacenados
		self.highscore_objects = []
		self.set_main_background()

		self.setup_main_music()
		self.setup_labels()
		self.__setUp()

	def __setUp(self):
		self.create_main_window()
		self.main_window_buttons()
		self.setup_main_window_music()
		self.create_highscore_window()
		self.hide_highscore_window()
		self.show()

	def button_click(self):
		self.music_dict["Click"].play()

	def set_main_background(self):
		palette = QPalette()
		pixmap = QPixmap("assets/main_background.jpg")
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
		self.selectmusicfolder.setStyleSheet(
			'QPushButton {background-color: #ae1165; color: white; font-size: 15pt; font-family: Comic Sans MS; border-syle: outset; border-width : 2px; border-color: blue; border-radius: 10px;} QPushButton:hover {background-color: #771165;}')
		self.main_window_objects.append(self.selectmusicfolder)

		self.first_row = QHBoxLayout(self)
		self.first_row.addWidget(self.playdccsells)
		self.first_row.addWidget(self.openhighscore)

		self.second_row = QHBoxLayout(self)
		self.second_row.addWidget(self.selectmusicfolder)
		self.second_row.addWidget(self.exitdccels)

		self.button_layout.addLayout(self.first_row)
		self.button_layout.addLayout(self.second_row)
		self.button_layout.setAlignment(Qt.AlignBottom)
		self.mainvbox.addLayout(self.button_layout)
		self.mainvbox.setSpacing(12.5)

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
		pixmap = QPixmap("assets/Highscorebackground.jpeg").scaled(700, 700)
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

	# self.highscore_buttom.hide()
	# self.label_dict["highscores logo"].hide()

	def setup_highscore_music(self):
		self.music_dict["Main Title"].stop()
		self.music_dict["Top 10"].play()


class GameWindow(QMainWindow):  # Launches game and game GUI
	pass


class ScoreWindow(QWidget):  # Changes to HighScore section
	def __init__(self):
		super().__init__()
		self.set_background()
		self.setup_music()
		self.setup_labels()
		self.__setUp()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	main_game = MainWindow()
	sys.exit(app.exec_())
