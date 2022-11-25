import pygame
from modules.UI.text import Text
from modules.settings import *

class Button(Text):
	def __init__(self, parent, pos=(0, 0), image=None, size=45):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.size = size

		self.image = pygame.image.load(image).convert_alpha()

		self.image = pygame.transform.scale(self.image, (self.image.get_width() * PPP, self.image.get_height() * PPP))

		self.pos = super().parse_pos(pos)

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		self.display_surface.blit(self.image, self.pos)