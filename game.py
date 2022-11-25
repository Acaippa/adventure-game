import pygame
from modules.menus.main_menu import MainMenu

class Game:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.delta_time = 0

		self.states = {
			"mainmenu" : MainMenu
		}

		self.current_state = self.states["mainmenu"]()

	def update(self, dt): # Update the current state
		self.delta_time = dt

		self.current_state.update(self.delta_time)

	def changeState(self, state): # Initiate the new state
		self.current_state = self.states[state]()
