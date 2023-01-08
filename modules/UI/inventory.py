from modules.UI.text import*

class inventory(Text):
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
			if index < 4 and slot.item == None:
				slot.item = item
				break

	# TODO add remove item

class Slot:
	def __init__(self, inventory, pos):
		self.inventory = inventory

		self.pos = pos

		self.display_surface = inventory.display_surface

		self.item = None

		self.slot = pygame.image.load("images/UI/inventory/slot.png").convert_alpha()

		self.delta_time = 0

		self.item_offset = 5

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		self.display_surface.blit(self.slot, self.pos)

		if self.item != None:
			self.display_surface.blit(self.item.image, self.pos)