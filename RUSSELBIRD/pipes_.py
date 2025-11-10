#pipes.py

import pygame
from settings_ import pipes_x, pipes_y, pipes_w, pipes_h


class Pipe(pygame.Rect):
    def __init__(self, img, phase_offset=0):
        super().__init__(pipes_x, pipes_y, pipes_w, pipes_h)
        self.img = img
        self.passed = False
        self.base_y = self.y
        self.spawn_time = pygame.time.get_ticks()
        self.phase_offset = phase_offset