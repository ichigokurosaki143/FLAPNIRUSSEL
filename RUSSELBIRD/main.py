#main.py

import pygame
from sys import exit
import os
from settings_ import *
from bird_ import Bird
from pipes_ import Pipe
from assets_ import load_assets
from game_funtions_ import draw, move, create_pp

pygame.init()
pygame.mixer.init()

# Center Window (optional)
os.environ['SDL_VIDEO_CENTERED'] = " "
pygame.display.set_mode((1, 1))

assets = load_assets()

window = pygame.display.set_mode((Game_Width, Game_Height))
pygame.display.set_caption("Russel In The Wonderland")

clock = pygame.time.Clock()

# == GAME VARIABLES ==
bird = Bird(assets["bird"])
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
jump_strength = -6
score = 0
high_score = 0
game_over = False

# == SCROLLING BACKGROUND VARIABLES ==
bg_x1 = 0
bg_x2 = Game_Width

# == SCROLLING GROUND VARIABLES ==
ground_x1 = 0
ground_x2 = Game_Width
ground_speed = 2
ground_height = 100 

create_pp_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pp_timer, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pp_timer and not game_over:
            create_pp(pipes, assets["top_pipe"], assets["bottom_pipe"])

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                velocity_y = jump_strength
                assets["flap"].play()

                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    bg_x1 = 0  # reset background
                    bg_x2 = Game_Width
                    ground_x1 = 0      
                    ground_x2 = Game_Width 
                    game_over = False
                    
    if not game_over:
        game_state = (velocity_y, score, 
                    high_score, game_over, 
                    velocity_x, gravity,
                    jump_strength, Pipe_Osc_Freq,
                    Pipe_Osc_Amp, ground_speed,)
        
        velocity_y, score, high_score, game_over, velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp, ground_speed = move(bird, pipes, assets, game_state)

        # --- NOW update background & ground positions using the NEW speeds ---
        # Background: slight parallax (slower), adjust multiplier if you want less/more parallax
        bg_multiplier = 0.6
        bg_x1 += velocity_x * bg_multiplier
        bg_x2 += velocity_x * bg_multiplier

        # Background wrap (keep them aligned)
        if bg_x1 <= -Game_Width:
            bg_x1 = bg_x2 + Game_Width

        if bg_x2 <= -Game_Width:
            bg_x2 = bg_x1 + Game_Width

        # Ground: use ground_speed (we set it equal to velocity_x in move())
        ground_x1 += ground_speed
        ground_x2 += ground_speed

        # Ground wrap (same pattern)
        if ground_x1 <= -Game_Width:
            ground_x1 = ground_x2 + Game_Width
            
        if ground_x2 <= -Game_Width:
            ground_x2 = ground_x1 + Game_Width


        draw(window, bird, pipes, assets, score, high_score, game_over, bg_x1, bg_x2, ground_x1, ground_x2)
        

    pygame.display.update()
    clock.tick(60)
