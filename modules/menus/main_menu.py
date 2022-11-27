import pygame
from modules.menus.menu import Menu
from modules.settings import * 
from modules.UI.text import *
from modules.UI.button import *

class MainMenu(Menu):
	def __init__(self, game):
		super().__init__(game)
		self.size = self.display_surface.get_size()
		self.surface = pygame.Surface(self.size)

		self.test_text = Text(self, pos=("center", 50), size=10)

	def on_update(self):
		self.draw_background(self.surface)

		self.test_text.update(self.delta_time)

	def on_draw(self):
		self.display_surface.blit(self.surface, self.pos)

	def draw_background(self, surface): # Scale background image correctly and paste it so it covers the whole background
		image = pygame.image.load("images/flooring.png").convert_alpha()
		image_dimentions = image.get_size()
		amount_of_images_x, amount_of_images_y = self.size[0] // image_dimentions[0], self.size[1] // image_dimentions[1]
		for x in range(amount_of_images_x + 1):
			for y in range(amount_of_images_y + 1):
				surface.blit(image, (image_dimentions[0] * x, image_dimentions[1] * y))