from modules.UI.text import*
from modules.settings import*
import pygame

class Inventory(Text):
	def __init__(self, parent, pos):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.background = pygame.image.load("images/UI/inventory/background.png").convert_alpha()

		self.pos = super().parse_pos(pos, self.background)

		self.slot_offset = 9

		self.slot_padding = 17

		self.slots = self.generate_slots()

	def update(self, dt):
		self.delta_time = dt

		self.draw()

		self.update_slots()

	def draw(self):
		self.display_surface.blit(self.background, self.pos)

	def generate_slots(self):
		temp = []
		for i in range(4):
			slot = Slot(self, ((self.pos[0] + self.slot_padding * i) + self.slot_offset, self.pos[1] + self.slot_offset))
			temp.append(slot)
		return temp

	def update_slots(self):
		for slot in self.slots:
			slot.update(self.delta_time)

	def add_item(self, item):
		for index, slot in enumerate(self.slots):
			if index < 4 and len(slot.items) == 0 or slot.items[0].name == item.name:
				slot.items.append(item)
				break

	def remove_item(self, item_to_remove):
		for slot in self.slots:
			for item in slot.items:
				if item == item_to_remove:
					slot.items.remove(item)

class Slot:
	def __init__(self, inventory, pos):
		self.inventory = inventory

		self.pos = pos

		self.display_surface = inventory.display_surface

		self.items = []

		self.slot = pygame.image.load("images/UI/inventory/slot.png").convert_alpha()

		self.rect = self.slot.get_rect(topleft = self.pos)

		self.delta_time = 0

		self.item_offset = (1, 0)

		self.font = pygame.font.Font("modules/fonts/joystix monospace.ttf", 10)

	def update(self, dt):
		self.delta_time = dt

		mouse = pygame.mouse.get_pos()

		if self.rect.collidepoint(mouse[0] / PPP, mouse[1] / PPP) and len(self.items) != 0:
			if self.inventory.parent.player.effect_duration_index < 0:
				self.items[0].on_used()

		self.draw()

		# Tegn mengden enheter i slottet
		offset = (self.pos[0] - 4, self.pos[1] - 6) # Gjør at tallet tegnes på hjørnet av slottet
		rendered_font = self.font.render((str(len(self.items))), True, "#FFFFFF") # Tallet som skal vises
		self.display_surface.blit(rendered_font, offset)


	def draw(self):
		self.display_surface.blit(self.slot, self.pos)

		if len(self.items) > 0:
			self.display_surface.blit(self.items[0].image, (self.pos[0] - self.item_offset[0], self.pos[1] - self.item_offset[1]))