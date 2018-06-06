from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

class Health_Bar(QGraphicsPixmapItem):

	def __init__(self,vida_max,largo):
		super().__init__()
		self.vida_max = vida_max
		self.largo = largo
		self.marco = QGraphicsPixmapItem(QPixmap("assets/vida/relleno.png").scaled(largo, 5), parent=self)
		self.setTransformOriginPoint(largo/2, largo/2)

	def update(self, vida):
		self.setPixmap(QPixmap("assets/vida/relleno.png").scaled(self.largo*(vida/self.vida_max), 5))

