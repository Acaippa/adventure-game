from .entity import Entity
from .enemies.broccoli import Broccoli
import pygame

class EnemySpawner01(Entity):
    def __init__(self, parent, pos):
        super().__init__(parent)

        self.parent.entity_list.append(self)

        self.player = self.parent.player

        self.pos = pos

        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

        self.spawn_time = 5

        self.spawn_time_index = 0
	
    def on_update(self):
        if self.spawn_time_index < self.spawn_time:
            self.spawn_time_index += 1 * self.delta_time
        else:
            self.parent.entity_list.append(Broccoli(self.parent, self.pos))
            self.spawn_time_index = 0