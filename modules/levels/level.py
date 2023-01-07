import pygame
from modules.levels.map_loader import *
from shortcuts import *
import math
from modules.settings import *
from modules.UI.health_bar import *
from modules.UI.inventory import *

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

		# self.map_loader.load_map(self.map)
		self.map_loader.load_csv("map/map..csv")

		self.inventory = inventory(self, ("left", "bottom"))

		self.health_bar = healthBar(self, self.player, pos=("left", 158))

	def update(self, dt):
		self.delta_time = dt

		self.surface.fill("black")

		self.camera.custom_draw(self.player, self.delta_time)

		self.health_bar.update(self.delta_time)

		self.inventory.update(self.delta_time)

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
			if math.hypot(self.parent.player.rect[0] - entity.rect[0], self.parent.player.rect[1] - entity.rect[1]) < 100:
				entity.update(self.delta_time)

			if hasattr(entity, "enemy") or hasattr(entity, "is_health_bar"):
				entity.update(self.delta_time)

			entity.draw(self.offset)