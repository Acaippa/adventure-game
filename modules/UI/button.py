import pygame
from modules.UI.text import Text
from modules.settings import *
from shortcuts import *
import random

class Button(Text):
	def __init__(self, parent, pos=(0, 0), image_paths=["images/buttons/play-button.png", "images/buttons/play-button-hover.png", "images/buttons/play-button-click.png"], size=45):
		self.parent = parent

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.size = size

		self.images = {}

		self.states = ["normal", "hover", "clicked"]

		self.state = ["normal"]

		for index, path in enumerate(image_paths): # load all images. Normal, Hover and Clicked
			self.images[self.states[index]] = pygame.image.load(path).convert_alpha()

		self.pos = super().parse_pos(pos)

		self.rect = scale_rect(self.images[self.state].get_rect(center=self.pos), PPP) # Scale the rect so that it matches the size on the screen.

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		self.display_surface.blit(self.image, center(self.pos, self.image))