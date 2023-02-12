import pygame
from .entity import Entity
from modules.animation.animation_handler import Animation
from modules.data_types.int_float import intFloat
import math
from modules.settings import*
from shortcuts import*
import os

class Player(Entity):
	def __init__(self, parent, start_pos=None):
		super().__init__(parent)

		self.player = None

		self.parent = parent

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

		self.attacking = False

		self.hurting = False

		self.attack_offset = 5

		self.default_force = 20

		self.default_knockback = 10

		self.force = self.default_force

		self.knockback = self.default_knockback

		self.effect_duration_index = 0

		self.effects = {
			"force" : "self.default_force", 
			"knockback" : "self.default_knockback", 
		}

	def on_update(self):
		self.animation_state = "idle"

		self.handle_effects()

		self.handle_input()

		self.turn_towards_pos(pygame.mouse.get_pos(), (self.pos[0] * PPP, self.pos[1] * PPP))

		self.handle_attack()

		if self.attacking and self.animation_handler.animation_index == self.attack_offset:
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

	def face_right(self):
		self.facing = "r"
		self.check_walk_horizontally()

	def face_left(self):
		self.facing = "l"
		self.flipped = True
		self.check_walk_horizontally()

	def face_up(self):
		self.facing = "u"
		self.animation_state = "idle_up"
		self.check_walk_vertically()

	def face_down(self):
		self.facing = "d"
		self.animation_state = "idle_down"
		self.check_walk_vertically()

	def check_walk_horizontally(self):
		if self.direction[0] != 0 or self.direction[1] != 0:
			self.animation_state = "walk_right"

	def check_walk_vertically(self):
		if self.direction[0] != 0 or self.direction[1] != 0:
			if self.facing == "u":
				self.animation_state = "walk_up"
			elif self.facing == "d":
				self.animation_state = "walk_down"



	def start_attack(self):
		if self.attacking == False:
			self.animation_handler.reset_animation()
			self.attacking = True
			self.hurting = True

	def handle_attack(self):
		if self.attacking and self.animation_handler.resat == False:
			if self.facing == "r" or self.facing == "l":
				self.animation_state = "attack_right"
			elif self.facing == "u":
				self.animation_state = "attack_up"
			elif self.facing == "d":
				self.animation_state = "attack_down"
		else:
			self.attacking = False

	def check_enemy_collision(self):
		for enemy in self.parent.enemy_list:
			offset = (enemy.rect.center[0] - self.rect.center[0], enemy.rect.center[1] - self.rect.center[1])
			overlap = self.mask.overlap(enemy.mask, offset)

			if overlap != None and self.hurting:
				enemy.hurt(self.force, self.knockback)
				self.hurting = False

	def handle_effects(self):
		if self.effect_duration_index > 0:
			self.effect_duration_index -= 1 * self.delta_time

		if self.effect_duration_index <= 0 and self.effect_duration_index != -42069:
			self.effect_duration_index = -42069
			self.reset_effects()
		
	def reset_effects(self):
		for effect in self.effects:
			setattr(self, effect, eval(self.effects[effect]))