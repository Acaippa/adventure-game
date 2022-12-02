import pygame
from modules.menus.main_menu import MainMenu
from modules.settings import *
from modules.levels.level import *

class Game:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.surface = pygame.Surface((self.display_surface.get_width() // PPP, self.display_surface.get_height() // PPP))

		self.delta_time = 0

		self.states = {
			"mainmenu" : MainMenu,
			"level" : Level
		}

		self.current_state = self.states["level"](self)

	def update(self, dt): # Update the current state
		self.delta_time = dt

		self.current_state.update(self.delta_time)

		self.draw()

	def changeState(self, state): # Initiate the new state
		self.current_state = self.states[state]()

	def draw(self):
		self.display_surface.blit(pygame.transform.scale(self.surface, self.display_surface.get_size()), (0, 0))
