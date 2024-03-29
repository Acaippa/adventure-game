import pygame
import os

class Animation:
    def __init__(self, entity, animation_path, speed=10): # Vent 10 frames før vi bytter til neste bilde
        self.entity = entity
        self.animation_path = animation_path
        self.default_speed = speed
        self.animation_index = 0
        self.delta_time = 0
        self.proxy_animation_index = 0
        self.resat = False

        self.images = {}

        self.config = self.entity.animation_config

        self.load_images()

    def update(self, dt):
        self.delta_time = dt

        self.animate_entity()

    def load_images(self): # Loop gjennom mappen der animasjonsstadiene ligger og lagre stadiet som nøkkelen til self.images og bildene som verdien til sistnevnte #! TODO: Cleanup 
        for state in os.listdir(self.animation_path):
            state_path = os.path.join(self.animation_path, state)
            self.images[state] = [pygame.image.load(os.path.join(self.animation_path, state, image)) for image in os.listdir(state_path)] # "idle_animation" : [01.png, 02.png, 03.png]


    def animate_entity(self):
        current_animation_state = self.entity.animation_state

        current_animation_images = self.images[current_animation_state]

        if current_animation_state in self.config:
            speed = int(self.config[current_animation_state]["speed"])
        else:
            speed = self.default_speed

        if self.animation_index < len(current_animation_images): # Om self.animation_index er mindre enn mengden bilder i nåværende statie, endre bilde til self.animation_index og incrementer self.animation_index
            self.entity.image = current_animation_images[self.animation_index]

            self.proxy_animation_index += speed * self.delta_time
            self.animation_index = round(self.proxy_animation_index)
            self.resat = False

        else: # Resett self.animation_index om animasjonen er ferdig
            self.animation_index = 0
            self.proxy_animation_index = 0
            self.resat = True

    def reset_animation(self):
        self.animation_index = 0
        self.proxy_animation_index = 0

    def parse_config(self):
        config_path = os.path.join(self.animation_path, )