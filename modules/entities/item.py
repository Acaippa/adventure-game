from modules.entities import Entity 
import pygame 

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