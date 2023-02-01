from modules.entities.enemy import Enemy
import os

class Broccoli(Enemy):
	def __init__(self, parent, pos):
		super().__init__(parent, pos, os.path.join("images", "enemies", "broccoli"))

		self.animation_config["walk_right"] = {"speed" : 3}