import pygame

class Menu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.delta_time = 0
		self.pos = (0, 0)

	def update(self, dt):
		self.delta_time = dt
		self.on_update()

		self.draw()

	def draw(self):
		self.on_draw()