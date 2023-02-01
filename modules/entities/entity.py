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

		self.turn_angles = {"-45 0" : self.face_right, "0 45" : self.face_right, "45 135" : self.face_down, "135 180" : self.face_left, "-180 -135" : self.face_left, "-135 -45" : self.face_up}

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

	def turn_towards_pos(self, pos2, pos1=None):
		self.flipped = False

		pos1 = (self.rect[0], self.rect[1]) if pos1 == None else pos1

		angle_to_pos = math.degrees(get_angle(pos1, pos2))
		for angle in self.turn_angles:
			from_, to = int(angle.split(" ")[0]), int(angle.split(" ")[1])
			if angle_to_pos > from_ and angle_to_pos < to:
				self.turn_angles[angle]()
	

	def face_up(self):
		self.facing = "u"
		self.on_face_up()

	def face_down(self):
		self.facing = "d"
		self.on_face_down()

	def face_left(self):
		self.facing = "l"
		self.on_face_left()

	def face_right(self):
		self.facing = "r"
		self.on_face_right()

	def on_face_up(self):
		pass

	def on_face_down(self):
		pass

	def on_face_right(self):
		pass

	def on_face_left(self):
		pass
