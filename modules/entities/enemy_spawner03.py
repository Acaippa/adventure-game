from .entity import Entity
from pygame import Rect

class EnemySpawner03(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.pos = pos

		self.rect = Rect(1, 1, pos[0], pos[1])