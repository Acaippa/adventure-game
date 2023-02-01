import pygame
from .entity import Entity
from random import randint, randrange
from shortcuts import center_bottom

class Tree(Entity):
	def __init__(self, parent, pos):
		super().__init__(parent)

		self.parent = parent

		self.parent.obsticle_list.append(self)

		self.image = pygame.image.load(f"images/environment/tree0{randint(1, 3)}.png").convert_alpha()

		self.random_offset = 10

		self.pos = pos[0] + round(randrange(-self.random_offset, self.random_offset)), pos[1] + round(randrange(-self.random_offset, self.random_offset))

		self.rect = self.image.get_rect(center=self.pos)

		self.rect.height = 15

		self.obsticle = None

	def on_draw(self, offset):
		self.display_surface.blit(self.image, center_bottom(self.rect.midbottom - offset, self.image))