import pygame
from game import Game

class Display:
	def __init__(self, dimentions=(900, 600)):
		pygame.init()
		self.display_surface = pygame.display.set_mode(dimentions)

		self.game = Game()

		self.real_fps = 0

		self.fps = 60

		self.running = True
		self.delta_time = 0
		self.clock = pygame.time.Clock()

	def main_loop(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			self.game.update(self.delta_time)

			self.real_fps = self.clock.get_fps()

			self.delta_time = self.clock.tick(self.fps) / 1000

			pygame.display.flip()


