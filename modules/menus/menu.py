import pygame

class Menu:
	def __init__(self, on_update=None, on_draw=None):
		self.display_surface = pygame.display.get_surface()
		self.delta_time = 0

		self.on_update = on_update
		self.on_draw = on_draw

	def update(self, dt):
		self.delta_time = dt
		self.on_update()

	def draw(self):
		self.on_draw()