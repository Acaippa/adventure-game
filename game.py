import pygame

class Game:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.delta_time = 0

		self.states = {
			"mainmenu" : MainMenu
		}

		self.current_state = self.states["mainmenu"]()

	def update(self, dt):
		self.delta_time = dt

	def changeState(self, state):
		self.current_state = self.states[state]()
