#assets.py

import pygame
from settings_ import Game_Width, Game_Height, bird_w, bird_h, pipes_w, pipes_h

def load_assets():
    # === IMAGES ===

    # Import background image
    bg = pygame.image.load("IMAGES/flappybirdbg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (Game_Width, Game_Height))

    # Import ground image
    ground = pygame.image.load("IMAGES/ground.png").convert_alpha()
    ground = pygame.transform.scale(ground, (Game_Width, 100))
    
    # Import bird image
    bird = pygame.image.load("IMAGES/russel.png").convert_alpha()
    bird = pygame.transform.scale(bird, (bird_w, bird_h))

    # Import pipe images
    top_pipe = pygame.image.load("IMAGES/top.png").convert_alpha()
    top_pipe = pygame.transform.scale(top_pipe, (pipes_w, pipes_h))

    # Import bottom pipe image
    bottom_pipe = pygame.image.load("IMAGES/bottom.png").convert_alpha()
    bottom_pipe = pygame.transform.scale(bottom_pipe, (pipes_w, pipes_h))

    # === SOUNDS ===
    
    flap = pygame.mixer.Sound("SFX/sfx_wing.wav")
    point = pygame.mixer.Sound("SFX/sfx_point.wav")
    hit = pygame.mixer.Sound("SFX/sfx_hit.wav")
    swoosh = pygame.mixer.Sound("SFX/sfx_swooshing.wav")
    die = pygame.mixer.Sound("SFX/sfx_die.wav")

    return {
        "bg": bg,
        "ground": ground,
        "bird": bird,
        "top_pipe": top_pipe,
        "bottom_pipe": bottom_pipe,
        "flap": flap,
        "point": point,
        "hit": hit,
        "swoosh": swoosh,
        "die": die
    }
