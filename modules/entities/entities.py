import pygame
from shortcuts import *
import random

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

		self.obsticle_list = self.parent.obsticle_list

		self.parent.entity_list.append(self)

		self.image = pygame.image.load("images/player/player_front.png").convert_alpha()

		self.pos = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2) # Center the player

		self.rect = self.image.get_rect()

		self.rect = self.rect.inflate((-10, -10))

		self.direction = [0, 0]

	def on_update(self):
		self.handle_input()

		self.draw()

	def on_draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))

	def handle_input(self): # Handle input AND collision
		input = pygame.key.get_pressed()

		movement = {pygame.K_UP : self.move_forwards, pygame.K_DOWN : self.move_backwards, pygame.K_RIGHT : self.move_right, pygame.K_LEFT : self.move_left}

		self.direction = [0, 0]

		for key in movement:
			if input[key]:
				movement[key]()


		self.rect.x += self.direction[0]
		self.handle_collision("x")
		self.rect.y += self.direction[1]
		self.handle_collision("y")


	def move_forwards(self):
		self.direction[1] = -1

	def move_backwards(self):
		self.direction[1] = 1

	def move_right(self):
		self.direction[0] = 1

	def move_left(self):
		self.direction[0] = -1

	def handle_collision(self, direction):
		if direction == "x":
			for obsticle in self.obsticle_list:
				if self.rect.colliderect(obsticle.rect):
					if self.direction[0] > 0:
						self.rect.right = obsticle.rect.left
					if self.direction[0] < 0:
						self.rect.left = obsticle.rect.right

		if direction == "y":
			for obsticle in self.obsticle_list:
				if self.rect.colliderect(obsticle.rect):
					if self.direction[1] > 0:
						self.rect.bottom = obsticle.rect.top
					if self.direction[1] < 0:
						self.rect.top = obsticle.rect.bottom

class Tree(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.image = pygame.image.load(f"images/environment/tree0{random.randint(1, 3)}.png").convert_alpha()

		self.pos = pos

		self.rect = self.image.get_rect(center=self.pos)

		self.rect.height = 15

		self.obsticle = None

	def on_draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))


