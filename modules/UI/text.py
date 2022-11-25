import pygame

class Text:
	def __init__(self, parent, pos=(0, 0), text="Lorem ipsum", color="white", size=45):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.pos = self.parse_pos(pos)

		self.text = text
		self.color = color
		self.size = size

		self.font = pygame.font.Font("modules/fonts/joystix monospace.ttf", size)

		self.blit_pos = (0, 0)

	def update(self, dt):
		self.delta_time = dt
		self.update_text()

		self.update_pos()

		self.draw()

	def draw(self):
		self.display_surface.blit(self.rendered_font, self.blit_pos)

	def parse_pos(self, pos): # Convert position from "center" to the center coordinates for the screen and so on
		positions = {"center" : self.parse_center, "top" : self.parse_top, "bottom" : self.parse_bottom, "right" : self.parse_right, "left" : self.parse_left}

		return_pos = {}

		for index, coord in enumerate(pos): # If the coord is text we have to convert it to an integer position relative to the pygame display surface by referring to the positions Dictionary
			print(pos)
			if isinstance(coord, str):
				return_pos[index] = positions[coord](index)
			elif isinstance(coord, int):
				return_pos[index] = coord

		return tuple([return_pos.get(item) for item in return_pos])

	def parse_center(self, index):
		return self.display_surface.get_size()[index] // 2

	def parse_top(self, index):
		return 0

	def parse_bottom(self, index):
		return self.display_surface.get_size()[1]

	def parse_right(self, index):
		return self.display_surface.get_size()[0]

	def parse_left(self, index):
		return 0

	def update_text(self):
		self.rendered_font = self.font.render(self.text, True, self.color)
		self.rendered_font_dimentions = self.rendered_font.get_size()


	def update_pos(self):
		self.blit_pos = self.pos[0] - self.rendered_font_dimentions[0] / 2, self.pos[1] - self.rendered_font_dimentions[1] / 2