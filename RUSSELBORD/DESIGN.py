#DESIGN

import pygame
from sys import exit
import random
import math

# === SETTINGS ===
Game_Width = 360
Game_Height = 640

# --- Initialize mixer ---
pygame.mixer.pre_init(44100, -16, 2, 512) #optional lang to
pygame.mixer.init()  # ensure mixer is initialized before loading sounds

# Liit ng opening (mas maliit, mas hirap)
Opening_Space = Game_Height / 5.2  # inadjust ko dati 1/4, ngayon mas maliit 

# Base oscillation settings (Ito yung nag papagalaw sa pipes sa pag taas at pag baba)
Pipe_Osc_Amp = 30 
Pipe_Osc_Freq = 0.002

# === GAME CONSTANTS ===
bird_x = Game_Width / 8
bird_y = Game_Height / 2
bird_w = 34
bird_h = 24

pipes_x = Game_Width
pipes_y = 0
pipes_w = 64
pipes_h = 512


# === CLASSES ===
class Bird(pygame.Rect):
    def __init__(self, img):
        super().__init__(bird_x, bird_y, bird_w, bird_h)
        self.img = img


class Pipe(pygame.Rect):
    def __init__(self, img, phase_offset=0):
        super().__init__(pipes_x, pipes_y, pipes_w, pipes_h)
        self.img = img
        self.passed = False
        self.base_y = self.y
        self.spawn_time = pygame.time.get_ticks()
        self.phase_offset = phase_offset


# === IMAGES ===
bg_img = pygame.image.load("flappybirdbg.png")
brd_img = pygame.image.load("russel.png")
brd_img = pygame.transform.scale(brd_img, (bird_w, bird_h))
top_pp_image = pygame.image.load("top.png")
top_pp_image = pygame.transform.scale(top_pp_image, (pipes_w, pipes_h))
bot_pp_image = pygame.image.load("bottom.png")
bot_pp_image = pygame.transform.scale(bot_pp_image, (pipes_w, pipes_h))

# == SOUNDS == 
flap_sound = pygame.mixer.Sound("sfx_wing.wav")
point_sound = pygame.mixer.Sound("sfx_point.wav")
hit_sound = pygame.mixer.Sound("sfx_hit.wav")
swoosh_sound = pygame.mixer.Sound("sfx_swooshing.wav")
die_sound = pygame.mixer.Sound("sfx_die.wav")

# === GAME STATE ===
bird = Bird(brd_img)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
jump_strength = -6
score = 0
high_score = 0
game_over = False


# === DRAW FUNCTION ===
def draw():
    window.blit(bg_img, (0, 0))
    window.blit(bird.img, bird)
    for pipe in pipes:
        window.blit(pipe.img, pipe)

    # === SCORE DISPLAY ===
    font_big = pygame.font.Font("flappy-font.ttf", 48) if pygame.font.get_fonts() else pygame.font.SysFont("Comic Sans MS", 48)
    font_small = pygame.font.Font("flappy-font.ttf", 28) if pygame.font.get_fonts() else pygame.font.SysFont("Comic Sans MS", 28)

    if not game_over:
        # --- Current score on center top ---
        text = font_big.render(f"{int(score)}", True, (255, 255, 255))
        shadow = font_big.render(f"{int(score)}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(Game_Width / 2, 80))
        shadow_rect = shadow.get_rect(center=(Game_Width / 2 + 2, 82))
        window.blit(shadow, shadow_rect)
        window.blit(text, text_rect)
        
    else:
        # === GAME OVER SCOREBOARD ===
        board_w, board_h = 250, 200
        board_x, board_y = (Game_Width - board_w) / 2, (Game_Height - board_h) / 2

        pygame.draw.rect(window, (245, 222, 179), (board_x, board_y, board_w, board_h), border_radius=15)
        pygame.draw.rect(window, (222, 184, 135), (board_x, board_y, board_w, board_h), 4, border_radius=15)

        # --- GAME OVER TEXT ---
        title = font_big.render("GAME OVER", True, (255, 255, 255))
        title_shadow = font_big.render("GAME OVER", True, (0, 0, 0))
        title_rect = title.get_rect(center=(board_x + board_w / 2, board_y + 50))
        title_shadow_rect = title_shadow.get_rect(center=(board_x + board_w / 2 + 2, board_y + 52))

        window.blit(title_shadow, title_shadow_rect)
        window.blit(title, title_rect)

        # --- SCORE TEXTS ---
        score_text = font_small.render(f"Score: {int(score)}", True, (0, 0, 0))
        best_text = font_small.render(f"Best: {int(high_score)}", True, (0, 0, 0))

        score_rect = score_text.get_rect(center=(board_x + board_w / 2, board_y + 105))
        best_rect = best_text.get_rect(center=(board_x + board_w / 2, board_y + 135))

        window.blit(score_text, score_rect)
        window.blit(best_text, best_rect)

        # --- RESTART TEXT---
        restart_font = pygame.font.Font("flappy-font.ttf", 20) if pygame.font.get_fonts() else pygame.font.SysFont("Comic Sans MS", 20)
        restart_text = restart_font.render("Press SPACE to Restart", True, (80, 60, 40))
        restart_rect = restart_text.get_rect(center=(board_x + board_w / 2, board_y + board_h - 25))
    
        window.blit(restart_text, restart_rect)


# === MOVE FUNCTION ===
def move():
    global velocity_y, score, high_score, game_over, velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp

    # --- Difficulty scaling (habang tumataas score, bumibilis lahat) ---
    if score < 5:
        velocity_x = -2
        gravity = 0.4
        jump_strength = -6
        Pipe_Osc_Freq = 0.002
        Pipe_Osc_Amp = 30

    elif score < 10:
        velocity_x = -2.8
        gravity = 0.42
        jump_strength = -6.3
        Pipe_Osc_Freq = 0.0023
        Pipe_Osc_Amp = 32

    elif score < 15:
        velocity_x = -3.3
        gravity = 0.45
        jump_strength = -6.6
        Pipe_Osc_Freq = 0.0026
        Pipe_Osc_Amp = 34

    elif score < 20:
        velocity_x = -3.8
        gravity = 0.48
        jump_strength = -6.9
        Pipe_Osc_Freq = 0.0029
        Pipe_Osc_Amp = 36

    else:
        velocity_x = -4.3
        gravity = 0.5
        jump_strength = -7.2
        Pipe_Osc_Freq = 0.0032
        Pipe_Osc_Amp = 38

    # --- Galaw ni bird ---
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > Game_Height:
        game_over = True
        return

    # --- Galaw ng mga pipes ---
    movement_pp = 0
    while movement_pp< len(pipes):
        top_pipe = pipes[movement_pp]
        bot_pipe = pipes[movement_pp + 1] if movement_pp + 1 < len(pipes) else None

        # X-axis galaw
        top_pipe.x += velocity_x
        if bot_pipe:
            bot_pipe.x = top_pipe.x

        # Y-axis galaw (oscillation pag score ≥ 10)
        if score >= 10:
            elapsed = (pygame.time.get_ticks() - top_pipe.spawn_time)
            offset = math.sin(elapsed * Pipe_Osc_Freq + top_pipe.phase_offset) * Pipe_Osc_Amp
            top_pipe.y = top_pipe.base_y + offset
            if bot_pipe:
                bot_pipe.y = top_pipe.y + top_pipe.h + Opening_Space
        else:
            top_pipe.y = top_pipe.base_y
            if bot_pipe:
                bot_pipe.y = bot_pipe.base_y

        # Scoring check (per pipe pair)
        if not top_pipe.passed and bird.x > top_pipe.x + pipes_w:
            point_sound.play()  # kapag nakascore
            score += 1
            top_pipe.passed = True
            if bot_pipe:
                bot_pipe.passed = True

        # Collision detection
        if bird.colliderect(top_pipe) or (bot_pipe and bird.colliderect(bot_pipe)):
            hit_sound.play()  # sound kapag nabangga
            die_sound.play()  # death sound

            if score > high_score:
                high_score = score

            game_over = True
            return

        movement_pp += 2

    # Alisin yung mga off-screen pipes
    while len(pipes) >= 2 and pipes[0].x < -pipes_w:
        pipes.pop(0)
        pipes.pop(0)


# === PIPE CREATION ===
def create_pp():
    # Random y position para hindi pare-pareho
    random_pp_y = pipes_y - pipes_h / 4 - random.random() * (pipes_h / 2)
    phase_offset = random.uniform(0, math.pi * 2)

    top_pp = Pipe(top_pp_image, phase_offset)
    top_pp.y = random_pp_y
    top_pp.base_y = top_pp.y
    pipes.append(top_pp)

    bot_pp = Pipe(bot_pp_image, phase_offset)
    bot_pp.y = top_pp.y + top_pp.h + Opening_Space
    bot_pp.base_y = bot_pp.y
    pipes.append(bot_pp)


# === MAIN LOOP ===
pygame.init()
window = pygame.display.set_mode((Game_Width, Game_Height))
pygame.display.set_caption("Russel In The Wonderland")
clock = pygame.time.Clock()

create_pp_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pp_timer, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pp_timer and not game_over:
            create_pp()
        

        # == KEYBINDS == 
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                velocity_y = jump_strength
                flap_sound.play()

                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False

    if not game_over:
        move()
        draw()

    pygame.display.update()
    clock.tick(60)
