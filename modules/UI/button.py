import pygame
from modules.UI.text import Text
from modules.settings import *
from shortcuts import *
import random

class Button(Text):
	def __init__(self, parent, pos=(0, 0), images={"normal" : "images/buttons/play-button.png", "hover" : "images/buttons/play-button-hover.png", "click" : "images/buttons/play-button-click.png"}, size=45, **kwargs):
		self.parent = parent

		self.parent.item_list.append(self)

		self.display_surface = self.parent.surface

		self.delta_time = 0

		self.size = size

		self.images = {}

		self.state = "normal"

		for path in images: # load all images. Normal, Hover and Clicked
			self.images[path] = pygame.image.load(images[path]).convert_alpha()

		self.pos = super().parse_pos(pos)

		self.rect = scale_rect(self.images[self.state].get_rect(center=self.pos), PPP) # Scale the rect so that it matches the size on the screen.

		self.click_check = False

		self.cmd = kwargs.get('cmd', self.fallback)

	def update(self, dt):
		self.delta_time = dt

		self.detect_click()

		self.draw()

	def draw(self):
		self.display_surface.blit(self.images[self.state], center(self.pos, self.images[self.state]))

	def detect_click(self):
		mouse = pygame.mouse.get_pos()
		mouse_clicked = pygame.mouse.get_pressed()

		hover = self.rect.collidepoint(mouse)

		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.state = "hover"
		else:
			self.state = "normal"

		if hover and mouse_clicked[0]:
			self.click_check = True
			self.state = "click"

		if hover and mouse_clicked[0] == False and self.click_check == True:
			self.cmd()
			self.click_check = False

		if hover == False:
			self.click_check = False

	def fallback(self):
		pass
 
