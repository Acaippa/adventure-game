import pygame

class Level:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.surface = pygame.Surface(self.display_surface.get_size())

		self.delta_time = 0

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		self.display_surface.blit(self.surface, (0, 0))

class Camera:
	def __init__(self)