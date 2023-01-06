from modules.UI.text import * 

class healthBar(Text):
	def __init__(self, parent, entity, pos, background="images/UI/healthbarplayer/healthbarbackground.png", foreground="images/UI/healthbarplayer/healthbarvalue.png"):
		self.entity = entity

		self.parent = parent

		self.display_surface = self.parent.surface

		self.background_path = background
		self.foreground_path = foreground

		self.background = pygame.image.load(self.background_path).convert_alpha()
		self.foreground = pygame.image.load(self.foreground_path).convert_alpha()

		self.background = pygame.transform.scale2x(self.background)
		self.foreground = pygame.transform.scale2x(self.foreground)

		self.background_rect = self.background.get_rect()
		self.foreground_rect = self.foreground.get_rect()

		self.pos = super().parse_pos(pos, self.background)

		self.foreground_offset = 10

		self.foreground_width = self.foreground.get_width()

	def update(self, dt):
		self.delta_time = dt

		self.foreground = pygame.transform.scale(self.foreground, (self.foreground_width / self.entity.max_health * self.entity.health, self.pos[1]))

		self.draw()

	def draw(self):
		self.display_surface.blit(self.background, self.pos)
		self.display_surface.blit(self.foreground, (self.pos[0] + self.foreground_offset, self.pos[1]))

class floatingHealthBar:
	def __init__(self, parent, entity, image_offset=(0, 0)):
		self.parent = parent
		self.entity = entity

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.background = pygame.Surface((10, 2))
		self.foreground = pygame.Surface((10, 2))

		self.foreground_width = self.foreground.get_width()

		self.rect = self.background.get_rect(topleft = self.entity.pos)

		self.background.fill("#ffffff")
		self.foreground.fill("#ff0000")

		self.parent.entity_list.append(self)

		self.image_offset = image_offset

		self.is_health_bar = ""

	def update(self, dt):
		self.delta_time = dt

		self.rect = self.background.get_rect(topleft = self.entity.pos)

		self.foreground = pygame.transform.scale(self.foreground, (self.foreground_width / self.entity.max_health * self.entity.health, self.foreground.get_height()))

	def draw(self, offset):
		self.display_surface.blit(self.background, ((self.entity.rect[0], self.entity.rect[1]) - offset) + self.image_offset)
		self.display_surface.blit(self.foreground, ((self.entity.rect[0], self.entity.rect[1]) - offset) + self.image_offset)
