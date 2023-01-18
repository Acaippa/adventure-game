import pygame
from shortcuts import *
import random
import math
from modules.data_types.int_float import*
from modules.UI.health_bar import*
from modules.animation.animation_handler import*
import os
from modules.settings import*
 
class Entity:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.facing = "r"

		self.flipped = False

		self.health = 100

		self.max_health = 100

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

	def handle_collision(self, direction):
		if direction == "x":
			for obsticle in self.obsticle_list:
				if self.rect.colliderect(obsticle.rect):
					if self.direction[0] > 0:
						self.rect.right = obsticle.rect.left
						self.proxy_pos_x.return_value = self.rect.topleft[0]
					if self.direction[0] < 0:
						self.rect.left = obsticle.rect.right
						self.proxy_pos_x.return_value = self.rect.topleft[0]

		if direction == "y":
			for obsticle in self.obsticle_list:
				if self.rect.colliderect(obsticle.rect):
					if self.direction[1] > 0:
						self.rect.bottom = obsticle.rect.top
						self.proxy_pos_y.return_value = self.rect.topleft[1]
					if self.direction[1] < 0:
						self.rect.top = obsticle.rect.bottom
						self.proxy_pos_y.return_value = self.rect.topleft[1]

	def flip_image(self):
		if self.direction[0] < 0:
			self.facing = "l"
			
		elif self.direction[0] > 0:
			self.facing = "r"

		if self.facing == "l":
			self.image_rotated = pygame.transform.flip(self.image, True, False)

		if self.facing == "r":
			self.image_rotated = self.image


class Player(Entity):
	def __init__(self, parent, start_pos=None):
		super().__init__(parent)

		self.player = None

		self.parent = parent

		self.obsticle_list = self.parent.obsticle_list

		self.parent.entity_list.append(self)

		self.image = pygame.image.load("images/player/idle/01.png").convert_alpha()

		self.image_rotated = self.image

		self.mask = pygame.mask.from_surface(self.image_rotated)

		self.pos = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2) # Center the player

		self.rect = self.image.get_rect(center=self.pos)

		self.rect = self.rect.inflate((-10, -10))

		self.rect.center = start_pos

		self.direction = pygame.math.Vector2()

		self.proxy_pos_x = intFloat(self.rect[0])
		self.proxy_pos_y = intFloat(self.rect[1])

		self.speed = 1.5

		self.animation_handler = Animation(self, f"{os.getcwd()}\\images\\player")

		self.turn_angles = {"-45 0" : self.face_right, "0 45" : self.face_right, "45 135" : self.face_down, "135 180" : self.face_left, "-180 -135" : self.face_left, "-135 -45" : self.face_up}

		self.facing = "r"

		self.attacking = False

		self.attack_offset = 4

	def on_update(self):
		self.animation_state = "idle"

		self.handle_input()

		self.turn_towards_cursor()

		self.handle_attack()

		self.check_enemy_collision()

		self.animation_handler.update(self.delta_time)

		self.draw(0)

	def on_draw(self, offset):
		self.image_rotated = pygame.transform.flip(self.image, self.flipped, False)
		self.mask = pygame.mask.from_surface(self.image_rotated)
		self.display_surface.blit(self.image_rotated, center(self.pos, self.image_rotated))

	def handle_input(self): # !Handle input AND collision
		input = pygame.key.get_pressed()

		movement = {pygame.K_w : self.move_forwards, pygame.K_s : self.move_backwards, pygame.K_d : self.move_right, pygame.K_a : self.move_left}

		actions = {
			pygame.mouse.get_pressed()[0] == True : self.start_attack
		}

		self.direction = pygame.math.Vector2(0, 0)

		for key in movement:
			if input[key]:
				movement[key]()

		for key in actions:
			if key == True:
				actions[key]()

		if self.direction.length_squared() > 0:
			self.direction.scale_to_length(self.speed)

		# Split movement into two steps making it possible to handle collision in only one direction at a time.
		self.proxy_pos_x += self.direction[0]
		self.proxy_pos_y += self.direction[1]

		self.rect.x = self.proxy_pos_x.get()
		self.handle_collision("x")
		self.rect.y = self.proxy_pos_y.get()
		self.handle_collision("y")


	def move_forwards(self):
		self.direction[1] = -self.speed * self.delta_time

	def move_backwards(self):
		self.direction[1] = self.speed * self.delta_time

	def move_right(self):
		self.direction[0] = self.speed * self.delta_time

	def move_left(self):
		self.direction[0] = -self.speed * self.delta_time

	def turn_towards_cursor(self):
		self.flipped = False
		angle_to_cursor = math.degrees(get_angle((self.pos[0] * PPP, self.pos[1] * PPP), pygame.mouse.get_pos()))
		for angle in self.turn_angles:
			from_, to = int(angle.split(" ")[0]), int(angle.split(" ")[1])
			if angle_to_cursor > from_ and angle_to_cursor < to:
				self.turn_angles[angle]()

	def face_right(self):
		self.facing = "r"
		self.check_walk_horizontally()

	def face_left(self):
		self.facing = "l"
		self.flipped = True
		self.check_walk_horizontally()

	def face_up(self):
		self.facing = "u"
		self.animation_state = "idle_back"
		self.check_walk_vertically()

	def face_down(self):
		self.facing = "d"

	def check_walk_horizontally(self):
		if self.direction[0] != 0 or self.direction[1] != 0:
			self.animation_state = "walk"

	def check_walk_vertically(self):
		if self.direction[0] != 0 or self.direction[1] != 0:
			self.animation_state = "walk_back"

	def start_attack(self):
		if self.attacking == False:
			self.animation_handler.reset_animation()
			self.attacking = True

	def handle_attack(self):
		if self.attacking and self.animation_handler.resat == False:
			if self.facing == "r" or self.facing == "l":
				self.animation_state = "attack_right"
			elif self.facing == "u":
				self.animation_state = "attack_up"
		else:
			self.attacking = False

	def check_enemy_collision(self):
		for enemy in self.parent.enemy_list:
			offset = (enemy.rect.center[0] - self.rect.center[0], enemy.rect.center[1] - self.rect.center[1])
			overlap = self.mask.overlap(enemy.mask, offset)
			print(overlap)


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

		self.obsticle_list = self.parent.obsticle_list

		self.player = self.parent.player

		self.pos = pos

		self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

		self.spawn_time = 5

		self.spawn_time_index = 0

	def on_update(self):
		if self.spawn_time_index < self.spawn_time:
			self.spawn_time_index += 1 * self.delta_time
		else:
			print("spawning") # !Spawn enemy here
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

		self.direction = pygame.math.Vector2()

		self.proxy_pos_x = intFloat(self.pos[0])
		self.proxy_pos_y = intFloat(self.pos[1])

		self.speed = 0.1

		self.angle_to_player = 0

		self.obsticle_list = self.parent.obsticle_list

		self.is_at_wanted_location = True

		self.wanted_position = (0, 0)

		self.enemy = ""

		self.health_bar = floatingHealthBar(self.parent, self, image_offset=(15, 0))

		self.health = 50

		self.parent.enemy_list.append(self)

	def on_update(self): # Move randomly if the player is not in range.
		if self.get_distance_to_entity(self, self.player) <= self.view_range:
			self.move_towards_player()

		else:
			self.move_randomly()

		self.flip_image()

		self.apply_movement()

	def on_draw(self, offset):
		self.mask = pygame.mask.from_surface(self.image_rotated)
		self.display_surface.blit(self.image_rotated, center(self.rect.center - offset, self.image))

	def move_towards_player(self):
		self.update_angle_to_player()

		self.direction[0] = math.cos(self.radians_to_player) * (self.speed * self.delta_time)
		self.direction[1] = math.sin(self.radians_to_player) * (self.speed * self.delta_time)

	def apply_movement(self):
		if self.direction.length_squared() > 0:
			self.direction.scale_to_length(self.speed)

		self.proxy_pos_x += self.direction[0]
		self.proxy_pos_y += self.direction[1]

		self.rect.x = self.proxy_pos_x.get()
		self.handle_collision("x")
		self.rect.y = self.proxy_pos_y.get()
		self.handle_collision("y")

	def update_angle_to_player(self):
		self.radians_to_player = math.atan2(self.player.rect.center[1] - self.rect.center[1], self.player.rect.center[0] - self.rect.center[0])

	def move_randomly(self): # Pick a random point inside its range and walk to that point.
		if self.is_at_wanted_location == True:
			position_is_in_bounds = False

			while position_is_in_bounds == False:
				self.wanted_position = (random.randint(self.pos[0], self.pos[0] + self.view_range), random.randint(self.pos[1], self.pos[1] + self.view_range))
				for obsticle in self.obsticle_list:
					if obsticle.rect.collidepoint(self.wanted_position) == False:
						position_is_in_bounds = True

			self.is_at_wanted_location = False
		else:
			angle_to_wanted_position = math.atan2(self.wanted_position[1] - self.rect[1], self.wanted_position[0] - self.rect[0])
			self.direction[0] = math.cos(angle_to_wanted_position) * (self.speed * self.delta_time)
			self.direction[1] = math.sin(angle_to_wanted_position) * (self.speed * self.delta_time)
			if self.rect.collidepoint(self.wanted_position):
				self.is_at_wanted_location = True


class Skeleton(Enemy):
	def __init__(self, parent, pos):
		super().__init__(parent, pos)

		self.image = pygame.image.load("images/enemies/skeleton01.png").convert_alpha()

		self.rect = self.image.get_rect(topleft = self.pos)

class Item(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)
		self.pos = pos

		self.parent = parent

		self.player = self.parent.player

		self.delta_time = 0

		self.is_item = ""

		# self.parent.entity_list.append(self)

		self.rect = pygame.Rect(self.pos[0], self.pos[1], 20, 20)

		self.image = pygame.image.load("images/player/player_front.png") # TODO change image

		# TODO make enemies drop different items

	def update(self, dt):
		self.delta_time = dt

		self.player = self.parent.player

		if self.player.rect.colliderect(self.rect):
			self.parent.inventory.add_item(self)
			self.parent.entity_list.remove(self)

	def on_draw(self, offset):
		self.display_surface.blit(self.image, self.pos - offset)
