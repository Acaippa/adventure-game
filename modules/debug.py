import pygame

class Debug:
    def __init__(self, surface, text):
        self.surface = surface
        self.font = pygame.font.SysFont(None, 20)
        self.rendered_font = self.font.render(str(text), True, "#ffffff")
        self.surface.blit(self.rendered_font, (0, 0))