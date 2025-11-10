#bird.py

import pygame
from settings_ import bird_x, bird_y, bird_w, bird_h


class Bird(pygame.Rect):
    def __init__(self, img):
        super().__init__(bird_x, bird_y, bird_w, bird_h)
        self.img = img