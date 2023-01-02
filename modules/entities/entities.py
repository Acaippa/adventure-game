import pygame
from shortcuts import *
import random
import math

class Entity:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

	def update(self, dt):
		self.delta_time = dt

		self.player = self.parent.player

		self.on_update()

	def draw(self, offset):
		self.on_draw(offset)

	def fallback(self): # Function that does nothing in order to prevent empty entities from crashing the program
		print(__name__, "Fallback")

	def on_draw(self, offset):
		pass

	def on_update(self):
		pass

	def get_distance_to_entity(self, entity1, entity2):
		return math.hypot(entity1.rect[1] - entity2.rect[1], entity1.rect[0] - entity2.rect[0])

class Player(Entity):
	def __init__(self, parent, start_pos=None):
		super().__init__(parent)

		self.player = None

		self.parent = parent

		self.obsticle_list = self.parent.obsticle_list

		self.parent.entity_list.append(self)

		self.image = pygame.image.load("images/player/player_front.png").convert_alpha()

		self.pos = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2) # Center the player

		self.rect = self.image.get_rect()

		self.rect = self.rect.inflate((-10, -10))

		self.rect.center = start_pos

		self.direction = [0, 0]

		self.speed = 70

	def on_update(self):
		self.handle_input()

		self.draw(0)

	def on_draw(self, offset):
		self.display_surface.blit(self.image, center(self.pos, self.image))

	def handle_input(self): # Handle input AND collision
		input = pygame.key.get_pressed()

		movement = {pygame.K_UP : self.move_forwards, pygame.K_DOWN : self.move_backwards, pygame.K_RIGHT : self.move_right, pygame.K_LEFT : self.move_left}

		self.direction = pygame.math.Vector2(0, 0)

		for key in movement:
			if input[key]:
				movement[key]()


		# Split movement into two steps making it possible to handle collision in only one direction at a time.
		self.rect.x += round(self.direction[0])
		self.handle_collision("x")
		self.rect.y += round(self.direction[1])
		self.handle_collision("y")


	def move_forwards(self):
		self.direction[1] = -self.speed * self.delta_time

	def move_backwards(self):
		self.direction[1] = self.speed * self.delta_time

	def move_right(self):
		self.direction[0] = self.speed * self.delta_time

	def move_left(self):
		self.direction[0] = -self.speed * self.delta_time

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

		self.parent = parent

		self.parent.obsticle_list.append(self)

		self.image = pygame.image.load(f"images/environment/tree0{random.randint(1, 3)}.png").convert_alpha()

		self.pos = pos

		self.rect = self.image.get_rect(center=self.pos)

		self.rect.height = 15

		self.obsticle = None

	def on_draw(self, offset):
		self.display_surface.blit(self.image, center_bottom(self.rect.midbottom - offset, self.image))


class EnemySpawner01(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.parent.entity_list.append(self)

		self.player = self.parent.player

		self.pos = pos

		self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

		self.spawn_time = 5

		self.spawn_time_index = 0

	def on_update(self):
		if self.spawn_time_index < self.spawn_time:
			self.spawn_time_index += 1 * self.delta_time
		else:
			print("spawning") # Spawn enemy here
			self.spawn_time_index = 0

class EnemySpawner02(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.pos = pos

		self.rect = pygame.Rect(1, 1, pos[0], pos[1])

class EnemySpawner03(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.pos = pos

		self.rect = pygame.Rect(1, 1, pos[0], pos[1])

class Enemy(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.pos = pos

		self.player = self.parent.player

		self.view_range = 100

		self.direction = [0, 0]

		self.speed = 50

	def on_update(self):
		if self.get_distance_to_entity(self, self.player) <= self.view_range:
			self.move_towards_player()

		self.apply_movement()

	def on_draw(self, offset):
		self.display_surface.blit(self.image, center_bottom(self.rect.midbottom - offset, self.image))

	def move_towards_player(self):
		self.direction[0] = self.speed * self.delta_time

	def apply_movement(self):
		self.rect.x += self.direction[0]
		self.rect.y += self.direction[1]

class Skeleton(Enemy):
	def __init__(self, parent, pos):
		super().__init__(parent, pos)

		self.image = pygame.image.load("images/enemies/skeleton01.png").convert_alpha()

		self.rect = self.image.get_rect(center = self.pos)