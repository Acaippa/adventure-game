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

		self.animation_config = {}

		self.shake_duration = .1

		self.shake_duration_index = 0

		self.shaking = False

	def update(self, dt):
		self.delta_time = dt

		self.player = self.parent.player

		self.on_update()

	def draw(self, offset):
		self.on_draw(offset)

	def die(self, skip=False):
		if not skip:
			if self in self.parent.entity_list:
				self.parent.entity_list.remove(self)
			self.on_die()
		else:
			self.on_die()

	def fallback(self): # Function that does nothing in order to prevent empty entities from crashing the program
		print(__name__, "Fallback")

	def on_draw(self, offset):
		pass

	def on_update(self):
		pass

	def on_die(self):
		pass

	def on_hurt(self, damage):
		pass

	def hurt(self, damage, skip=False): # If skip go straight to on_hurt
		if not skip:
			if self.health - damage < 0:
				self.die()
			else:
				self.health -= damage
			self.on_hurt(damage)
		else:
			self.on_hurt(damage)

	def get_distance_to_entity(self, entity1, entity2):
		return math.hypot(entity1.rect[1] - entity2.rect[1], entity1.rect[0] - entity2.rect[0])

	def handle_collision(self, direction):
		if len(self.parent.obsticle_list) != 0: # Bare sjekk kollisjon om det er obsticles å sjekke kollisjon imot
			if direction == "x":
				for obsticle in self.parent.obsticle_list:
					if self.rect.colliderect(obsticle.rect):
						if hasattr(self, "is_at_wanted_location"):
							self.is_at_wanted_location = True

						if self.direction[0] > 0:
							self.rect.right = obsticle.rect.left
							self.proxy_pos_x.return_value = self.rect.topleft[0]
						if self.direction[0] < 0:
							self.rect.left = obsticle.rect.right
							self.proxy_pos_x.return_value = self.rect.topleft[0]

			if direction == "y":
				for obsticle in self.parent.obsticle_list:
					if self.rect.colliderect(obsticle.rect):
						if hasattr(self, "is_at_wanted_location"):
							self.is_at_wanted_location = True
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
