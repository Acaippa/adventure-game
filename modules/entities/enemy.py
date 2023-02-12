from .entity import Entity 
import pygame
from modules.data_types.int_float import intFloat
from modules.UI.health_bar import FloatingHealthBar
from modules.animation.animation_handler import Animation
from random import randint, randrange
from shortcuts import center
from math import sin, cos, atan2

class Enemy(Entity):
	def __init__(self, parent, pos, animation_path):
		super().__init__(parent)

		self.pos = pos

		self.player = self.parent.player

		self.view_range = 100

		self.attack_range = 20

		self.direction = pygame.math.Vector2()

		self.proxy_pos_x = intFloat(self.pos[0])
		self.proxy_pos_y = intFloat(self.pos[1])

		self.speed = 0.1

		self.angle_to_player = 0

		self.is_at_wanted_location = True

		self.wanted_position = (0, 0)

		self.enemy = ""

		self.health_bar = FloatingHealthBar(self.parent, self, image_offset=(15, 0))

		self.health = 100

		self.parent.enemy_list.append(self)

		self.attack_delay = 2.5

		self.attack_delay_index = 0

		self.attacking = False

		self.hurting = False

		self.mask = pygame.Mask((20, 20))

		self.animation_path = animation_path

		self.animation_handler = Animation(self, self.animation_path)

		self.animation_state = "idle_right"

		self.animation_handler.update(self.delta_time)

		self.image_rotated = self.image

		self.rect = self.image.get_rect(topleft = self.pos)

		self.parent_entity_list = self.parent.entity_list

		self.sliding = False

		self.sliding_velocity = 0

		self.sliding_friction = 40

		self.sliding_angle = 0.1

		self.force = 1

	def on_update(self):
		self.animation_state = "idle_right"

		if self.get_distance_to_entity(self, self.player) <= self.view_range:
			self.move_towards_player()
			if self.get_distance_to_entity(self, self.player) <= self.attack_range:
				self.update_attack()
			elif self.attacking != False:
				self.attack_delay_index = self.attack_delay

		else:
			self.move_randomly()

		self.face_towards_direction()

		self.animation_handler.update(self.delta_time)

		self.apply_movement()

	def on_draw(self, offset):
		if self.shaking and self.shake_duration_index < self.shake_duration:
			shaking_offset = (randrange(-2, 2), randrange(-2, 2))
			self.shake_duration_index += 1 * self.delta_time
		else:
			self.shake_duration_index = 0
			self.shaking = False
			shaking_offset = (0, 0)

		self.mask = pygame.mask.from_surface(self.image_rotated)
		self.display_surface.blit(self.image_rotated, center(self.rect.center - offset - shaking_offset, self.image))

	def move_towards_player(self):
		self.update_angle_to_player()

		self.direction[0] = cos(self.radians_to_player) * (self.speed * self.delta_time)
		self.direction[1] = sin(self.radians_to_player) * (self.speed * self.delta_time)

		# ! self.turn_towards_pos(self.pos, (self.player.rect[0], self.player.rect[1]))

	def on_die(self):
		self.health_bar.die()

	def apply_movement(self):
		if self.direction.length_squared() > 0:
			self.direction.scale_to_length(self.speed)
		
		if self.sliding_velocity > 0.1:
			self.sliding_velocity -= self.sliding_friction * self.delta_time
			self.sliding = True
		else:
			self.sliding = False
			self.sliding_velocity = 0
		
		self.proxy_pos_x += self.direction[0] if self.sliding == False else cos(self.sliding_angle) * (self.sliding_velocity * -1 * self.delta_time)
		self.proxy_pos_y += self.direction[1] if self.sliding == False else sin(self.sliding_angle) * (self.sliding_velocity * -1 * self.delta_time)

		self.rect.x = self.proxy_pos_x.get()
		self.handle_collision("x")
		self.rect.y = self.proxy_pos_y.get()
		self.handle_collision("y")

	def update_angle_to_player(self):
		self.radians_to_player = atan2(self.player.rect.center[1] - self.rect.center[1], self.player.rect.center[0] - self.rect.center[0])

	def move_randomly(self): # Pick a random point inside its range and walk to that point.
		if self.is_at_wanted_location == True:
			#! TODO: Add - self.view_range
			self.wanted_position = (randint(self.pos[0], self.pos[0] + self.view_range), randint(self.pos[1], self.pos[1] + self.view_range))
			self.is_at_wanted_location = False
		else:
			angle_to_wanted_position = atan2(self.wanted_position[1] - self.rect[1], self.wanted_position[0] - self.rect[0])
			self.direction[0] = cos(angle_to_wanted_position) * (self.speed * self.delta_time)
			self.direction[1] = sin(angle_to_wanted_position) * (self.speed * self.delta_time)
			if self.rect.collidepoint(self.wanted_position):
				self.is_at_wanted_location = True

	def start_attack(self):
		self.attacking = True
		self.hurting = True
		self.attack_delay_index = 0
		self.animation_handler.reset_animation()

	def update_attack(self):
		if self.attack_delay_index < self.attack_delay:
			self.attack_delay_index += 1 * self.delta_time
		else:
			self.start_attack()

		offset = (self.player.rect.center[0] - self.rect.center[0], self.player.rect.center[1] - self.rect.center[1])
		overlap = self.mask.overlap(self.player.mask, offset)

		if self.attacking and overlap != None and self.hurting: # Stopp å skade spilleren om fienden treffer den 1 gang
			self.player.hurt(self.force, 0)
			self.hurting = False

		if self.animation_handler.resat: # Stopp attack
			self.attacking = False
			self.hurting = False

		if self.attacking: # Gjør at fienden spiller angrip animasjonen
			self.animation_state = "attack_right"

	def on_hurt(self, damage, knockback):
		self.shaking = True
		self.sliding = True
		self.sliding_velocity = knockback
		self.sliding_angle = atan2(self.player.rect.center[1] - self.rect.center[1], self.player.rect.center[0] - self.rect.center[0])

	def face_towards_direction(self):
		if self.direction[0] < 0:
			self.image_rotated = pygame.transform.flip(self.image, True, False)
		else:
			self.image_rotated = self.image

		if self.direction[1] < 0:
			self.animation_state = "walk_up"
		else:
			self.animation_state = "walk_down"