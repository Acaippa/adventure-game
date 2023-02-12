from modules.entities.entity import Entity 
import pygame

class Berry(Entity):
    def __init__(self, parent, pos, image, name, vel = 0):
        super().__init__(parent)

        self.pos = pos 

        self.velocity = vel

        self.image = pygame.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(center = self.pos)

        self.name = name

        self.effect_duration = 2

    def on_update(self):
        self.handle_pickup()

    def handle_pickup(self):
        length_to_player = super().get_distance_to_entity(self, self.player)

        if length_to_player < 50: # Plukk opp bæret
            self.parent.inventory.add_item(self)
            self.parent.entity_list.remove(self)

    def draw(self, offset):
        self.display_surface.blit(self.image, self.pos - offset)

    def on_used(self):
        self.on_on_used()
        self.player.knockback = 50
        self.player.effect_duration_index = self.effect_duration
        self.parent.inventory.remove_item(self)

    def on_on_used(self):
        pass