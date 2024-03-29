import pygame
from game import Game
from modules.debug import*

class Display:
	def __init__(self, dimentions=(1360, 800)):
		pygame.init()
		self.display_surface = pygame.display.set_mode(dimentions)

		self.game = Game()

		self.real_fps = 0

		self.fps = 60

		self.running = True
		self.delta_time = 0
		self.clock = pygame.time.Clock()

	def main_loop(self): # Check if the user wants to quit and update Game.py
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			self.game.update(self.delta_time)

			self.real_fps = self.clock.get_fps()

			Debug(self.display_surface, round(self.real_fps))

			self.delta_time = self.clock.tick(self.fps) / 1000

			pygame.display.flip()


