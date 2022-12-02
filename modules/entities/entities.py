import pygame
from shortcuts import *

class Entity:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

	def update(self, dt, pos=None):
		self.delta_time = dt
		self.pos = self.pos if pos == None else pos # If optional argument pos is defined redefine the position of the entity

		self.on_update()

		self.draw()

	def draw(self):
		self.on_draw()

	def fallback(self): # Function that does nothing in order to prevent empty entities from crashing the program
		print(__name__, "Fallback")

	def on_draw(self):
		pass

	def on_update(self):
		pass

class Player(Entity):
	def __init__(self, parent):
		super().__init__(parent)

		self.image = pygame.image.load("images/player/player_front.png").convert_alpha()

		self.pos = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2) # Center the player

		self.rect = self.image.get_rect(center=self.pos)

	def on_draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))

class Tree(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.image = pygame.image.load("images/environment/tree01.png").convert_alpha()

		self.pos = pos

		print(self.pos)

		self.rect = self.image.get_rect()

	def on_draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))


