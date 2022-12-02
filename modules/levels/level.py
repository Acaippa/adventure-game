import pygame
from modules.levels.map_loader import *

class Level:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.surface = pygame.Surface(self.display_surface.get_size())

		self.delta_time = 0

		self.player = None

		self.entity_list = []

		# TODO: add enemy_list

		self.map_loader = MapLoader(self)

		self.map = [
		["e t", "e t", "e t"],
		["e t", "p", "e t"],
		["e t", "e t", "e t"]
		]

		self.map_loader.load_map(self.map)

	def update(self, dt):
		self.delta_time = dt

		self.player.update(self.delta_time) # Update the player

		# Update the entities in self.entity_list
		for entity in self.entity_list:
			entity.update(self.delta_time)

		self.draw()

	def draw(self):
		self.display_surface.blit(self.surface, (0, 0))

class Camera:
	def __init__(self, parent):
		self.entity_list = [] # House all the entities the camera should draw

		self.parent = parent

		self.display_surface = self.parent.surface

		self.center_x, self.center_y = self.display_surface.get_width() / 2, self.display_surface.get_height() / 2

		self.delta_time = 0

		self.offset = pygame.math.Vector2()

	def custom_draw(self, player, dt):
		self.delta_time = dt

		self.offset.x, self.offset.y = player.rect[0] - self.center_x, player.rect[1] - self.center_y

		for entity in self.entity_list:
			entity.update(self.delta_time, pos=entity.pos - self.offset) # Pass in optional position argument to entity.