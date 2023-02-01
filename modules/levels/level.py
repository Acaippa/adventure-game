import pygame
from modules.levels.map_loader import MapLoader
from shortcuts import *
import math
from modules.settings import *
from modules.UI.health_bar import HealthBar
from modules.UI.inventory import Inventory
from modules.entities.image import Image

class Level:
	def __init__(self, parent):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.surface = pygame.Surface(self.display_surface.get_size())

		self.delta_time = 0

		self.player = None

		self.entity_list = []

		self.obsticle_list = []

		self.enemy_list = []

		self.camera = Camera(self)

		self.map_loader = MapLoader(self)

		self.map_loader.load_csv("map/map..csv")

		self.inventory = Inventory(self, ("left", "bottom"))

		self.health_bar = HealthBar(self, self.player, pos=("left", 158))

		self.background_image = Image(self, (0, 0), "images/map_new.png")

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

		self.parent.background_image.draw(self.offset)

		temp_obsticle_list = []

		for entity in sorted(self.entity_list, key = lambda entity: entity.rect.centery):
			length_to_entity = math.hypot(self.parent.player.rect[0] - entity.rect[0], self.parent.player.rect[1] - entity.rect[1])
			#! TODO add view and update range
			if length_to_entity < 100:
				entity.update(self.delta_time)
				if hasattr(entity, "obsticle"):
					temp_obsticle_list.append(entity)

			if hasattr(entity, "enemy") or hasattr(entity, "is_health_bar"):
				entity.update(self.delta_time)

			if length_to_entity < 200:
				entity.draw(self.offset)

		self.parent.obsticle_list = temp_obsticle_list
