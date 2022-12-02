import pygame
from shortcuts import *

class Entity:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

	def update(self, dt, pos=None):
		self.delta_time = dt
		
		if pos != None:
			pass

		self.on_update()

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

		self.player = None

		self.parent = parent

		self.parent.entity_list.append(self)

		self.image = pygame.image.load("images/player/player_front.png").convert_alpha()

		self.pos = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2) # Center the player

		self.rect = self.image.get_rect()

	def on_update(self):
		self.handle_input()

		self.draw()

	def on_draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))

	def handle_input(self):
		input = pygame.key.get_pressed()

		movement = {pygame.K_UP : self.move_forwards, pygame.K_DOWN : self.move_backwards, pygame.K_RIGHT : self.move_right, pygame.K_LEFT : self.move_left}

		for key in movement:
			if input[key]:
				movement[key]()

	def move_forwards(self):
		self.rect.y -= 1

	def move_backwards(self):
		self.rect.y += 1

	def move_right(self):
		self.rect.x += 1

	def move_left(self):
		self.rect.x -= 1

class Tree(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.image = pygame.image.load("images/environment/tree01.png").convert_alpha()

		self.pos = pos

		self.rect = self.image.get_rect(center=self.pos)

	def on_draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))


