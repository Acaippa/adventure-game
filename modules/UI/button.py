import pygame
from modules.UI.text import Text
from modules.settings import *
from shortcuts import *
import random

class Button(Text):
	def __init__(self, parent, pos=(0, 0), image="images/buttons/play-button.png", size=45):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.size = size

		self.image = pygame.image.load(image).convert_alpha()

		self.pos = super().parse_pos(pos)

		self.rect = scale_rect(self.image.get_rect(center=self.pos), PPP) # Scale the rect so that it matches the size on the screen.

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))