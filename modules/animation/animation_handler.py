import pygame
import os

class Animation:
    def __init__(self, entity, animation_path, speed=10): # Vent 10 frames før vi bytter til neste bilde
        self.entity = entity
        self.animation_path = animation_path
        self.speed = speed
        self.animation_index = 0
        self.delta_time = 0

        self.images = {}

        self.load_images()

    def update(self, dt):
        self.delta_time = dt

        self.animate_entity()

    def load_images(self): # Loop gjennom mappen der animasjonsstadiene ligger og lagre stadiet som nøkkelen til self.images og bildene som verdien til sistnevnte
        for state in os.listdir(self.animation_path):
            self.images[state] = os.listdir(f"{self.animation_path}\{state}") # "idle_animation" : [01.png, 02.png, 03.png]

    def animate_entity(self):
        current_animation_state = self.entity.animation_state

        current_animation_images = self.images[current_animation_state]

        if self.animation_index < len(current_animation_images): # Om self.animation_index er mindre enn mengden bilder i nåværende statie, endre bilde til self.animation_index og incrementer self.animation_index
            self.entity.image = current_animation_images[self.animation_index]
            self.animation_index += 1

        else: # Resett self.animation_index om animasjonen er ferdig
            self.animation_index = 0