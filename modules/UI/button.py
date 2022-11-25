import pygame
from modules.UI.text import Text

class Button(Text):
	def __init__(self, parent, pos=(0, 0), image=None, size=45):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.image = pygame.image.load(image).convert_alpha()

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		pass