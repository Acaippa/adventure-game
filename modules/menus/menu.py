import pygame

class Menu:
	def __init__(self, game):
		self.display_surface = game.surface
		self.delta_time = 0
		self.pos = (0, 0)
		self.item_list = []

	def update(self, dt):
		self.delta_time = dt

		self.on_update()

		for item in self.item_list:
			item.update(self.delta_time)

		self.draw()

	def draw(self):
		self.on_draw()