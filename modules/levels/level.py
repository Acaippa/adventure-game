import pygame
from modules.levels.map_loader import *
from shortcuts import *

class Level:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.surface = pygame.Surface(self.display_surface.get_size())

		self.delta_time = 0

		self.player = None

		self.entity_list = []

		self.obsticle_list = []

		self.camera = Camera(self)

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

		self.surface.fill("black")

		self.camera.custom_draw(self.player, self.delta_time)

		self.draw()

	def draw(self):
		self.display_surface.blit(self.surface, (0, 0))

class Camera:
	def __init__(self, parent):
		self.parent = parent

		self.entity_list = self.parent.entity_list

		self.obsticle_list = self.parent.obsticle_list

		self.parent = parent

		self.display_surface = self.parent.surface

		self.center_x, self.center_y = self.display_surface.get_width() / 2, self.display_surface.get_height() / 2

		self.delta_time = 0

		self.offset = pygame.math.Vector2()

	def custom_draw(self, player, dt):
		self.delta_time = dt

		self.offset.x, self.offset.y = player.rect.centerx - self.center_x, player.rect.centery - self.center_y

		for entity in sorted(self.entity_list, key = lambda entity: entity.rect.centery):
			if hasattr(entity, "player"):
				entity.update(self.delta_time)
				continue

			if hasattr(entity, "obsticle") and entity not in self.obsticle_list: # ! hardware intensive
				self.obsticle_list.append(entity)

			# pygame.draw.rect(self.display_surface, (255, 255, 255), pygame.Rect(entity.rect.x - self.offset[0], entity.rect.y - self.offset[1], entity.rect.width, entity.rect.height)) draw rect
			self.parent.surface.blit(entity.image, center(entity.rect.center - self.offset, entity.image)) # Pass in optional position argument to entity.