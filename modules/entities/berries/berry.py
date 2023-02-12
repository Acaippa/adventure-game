from modules.entities.entity import Entity
from shortcuts import get_angle, center
from math import cos, sin, hypot
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

        self.move_speed = 60

    def on_update(self):
        self.handle_pickup()
        print(self.length_to_player)

    def handle_pickup(self):
        self.length_to_player = super().get_distance_to_entity(self, self.player)

        if self.length_to_player < 20: # Beveg seg mot spilleren
            self.move_towards_player()

    def draw(self, offset):
        self.display_surface.blit(self.image, center(self.rect.center - offset, self.image))

    def move_towards_player(self):
        if self.length_to_player < 5:
            self.parent.inventory.add_item(self)
            self.parent.entity_list.remove(self)

        else:
            angle_to_player = get_angle(self.rect.center, self.player.rect.center)
            speed = self.move_speed - self.length_to_player

            self.pos = self.pos[0] + cos(angle_to_player) * speed * self.delta_time, self.pos[1] + sin(angle_to_player) * speed * self.delta_time

            self.rect.center = self.pos

    def on_used(self):
        self.on_on_used()
        self.player.effect_duration_index = self.effect_duration
        self.parent.inventory.remove_item(self)

    def on_on_used(self):
        pass