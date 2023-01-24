from .entities import*

class Image(Entity):
    def __init__(self, parent, pos, path):
        self.parent = parent
        super().__init__(self.parent)
        self.display_surface = self.parent.surface
        self.pos = pos
        self.image_path = path

        self.image = pygame.image.load(self.image_path).convert_alpha()

        self.rect = self.image.get_rect(topleft = self.pos)

    def draw(self, offset):
        self.display_surface.blit(self.image, self.pos - offset)