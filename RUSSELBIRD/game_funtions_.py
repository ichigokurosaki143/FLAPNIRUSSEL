#game_functions.py

import pygame, math, random
from settings_ import *
from pipes_ import Pipe

# Function to draw all game elements
def draw(window, bird, pipes, assets, score, high_score, game_over, bg_x1, bg_x2, ground_x1, ground_x2):
    
    # Draw scrolling background
    window.blit(assets["bg"], (bg_x1, 0))
    window.blit(assets["bg"], (bg_x2, 0))

    # Draw the pipes
    for pipe in pipes:
        window.blit(pipe.img, pipe)

    # Draw the bird
    window.blit(bird.img, bird)

    # Draw the ground
    window.blit(assets["ground"], (ground_x1, Game_Height - 62.5))
    window.blit(assets["ground"], (ground_x2, Game_Height - 62.5))
        
        
    # === SCORE DISPLAY ===
    font_big = pygame.font.Font("FONT/flappy-font.ttf", 48)
    font_small = pygame.font.Font("FONT/flappy-font.ttf", 28)

    # Draw current score
    if not game_over:
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
        
        # Draw the game over board
        pygame.draw.rect(window, (245, 222, 179), (board_x, board_y, board_w, board_h), border_radius=15)
        pygame.draw.rect(window, (222, 184, 135), (board_x, board_y, board_w, board_h), 4, border_radius=15)

        # Draw the game over text and scores
        title = font_big.render("GAME OVER", True, (255, 255, 255))
        title_shadow = font_big.render("GAME OVER", True, (0, 0, 0))
        title_rect = title.get_rect(center=(board_x + board_w / 2, board_y + 50))
        title_shadow_rect = title_shadow.get_rect(center=(board_x + board_w / 2 + 2, board_y + 52))
        # Display the title with shadow
        window.blit(title_shadow, title_shadow_rect)
        window.blit(title, title_rect)

        # Draw score and best score
        score_text = font_small.render(f"Score: {int(score)}", True, (0, 0, 0))
        best_text = font_small.render(f"Best: {int(high_score)}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(board_x + board_w / 2, board_y + 105))
        best_rect = best_text.get_rect(center=(board_x + board_w / 2, board_y + 135))
        # Display the texts
        window.blit(score_text, score_rect)
        window.blit(best_text, best_rect)

        # Draw restart instruction
        restart_font = pygame.font.Font("FONT/flappy-font.ttf", 20) if pygame.font.get_fonts() else pygame.font.SysFont("Comic Sans MS", 20)
        restart_text = restart_font.render("Press SPACE to Restart", True, (80, 60, 40))
        restart_rect = restart_text.get_rect(center=(board_x + board_w / 2, board_y + board_h - 25))
        # Display the restart instruction   
        window.blit(restart_text, restart_rect)

# Function to update game state
def move(bird, pipes, sounds, game_state):
    velocity_y, score, high_score, game_over, velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp, ground_speed = game_state

    if score < 5:
        velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp = -2, 0.4, -6, 0.002, 30

    elif score < 10:
        velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp = -2.8, 0.42, -6.3, 0.0023, 32

    elif score < 15:
        velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp = -3.3, 0.45, -6.6, 0.0026, 34

    elif score < 20:
        velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp = -3.8, 0.48, -6.9, 0.0029, 36

    else:
        velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp = -4.3, 0.5, -7.2, 0.0032, 38

    # === GROUND MOVEMENT ===
    ground_speed = velocity_x
    velocity_y += gravity
    # === BIRD MOVEMENT ===
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    # === GROUND COLLISION ===
    ground_y = Game_Height - 62.5 - bird_h  # ground height = 62.5
    if bird.y >= ground_y:
        bird.y = ground_y
        sounds["hit"].play()
        sounds["die"].play()
        if score > high_score:
            high_score = score
        game_over = True
        return velocity_y, score, high_score, game_over, velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp, ground_speed
    
    # === SKY COLLISION ===
    if bird.y <= 0:
        bird.y = 0
        sounds["hit"].play()
        sounds["die"].play()
        if score > high_score:
            high_score = score
        game_over = True
        return velocity_y, score, high_score, game_over, velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp, ground_speed

    # === PIPE MOVEMENT AND COLLISION ===
    movement_pp = 0
    while movement_pp < len(pipes):
        top_pipe = pipes[movement_pp]
        bot_pipe = pipes[movement_pp + 1] if movement_pp + 1 < len(pipes) else None
        top_pipe.x += velocity_x
        if bot_pipe:
            bot_pipe.x = top_pipe.x
        # --- PIPE OSCILLATION ---
        if score >= 10:
            elapsed = (pygame.time.get_ticks() - top_pipe.spawn_time)
            offset = math.sin(elapsed * Pipe_Osc_Freq + top_pipe.phase_offset) * Pipe_Osc_Amp
            top_pipe.y = top_pipe.base_y + offset
            if bot_pipe:
                bot_pipe.y = top_pipe.y + top_pipe.h + Opening_Space
        # --- PIPE COLLISION ---
        if not top_pipe.passed and bird.x > top_pipe.x + pipes_w:
            sounds["point"].play()
            score += 1
            top_pipe.passed = True
            if bot_pipe:
                bot_pipe.passed = True
        # --- CHECK FOR COLLISION ---
        if bird.colliderect(top_pipe) or (bot_pipe and bird.colliderect(bot_pipe)):
            sounds["hit"].play()
            sounds["die"].play()
            if score > high_score:
                high_score = score
            game_over = True
            return velocity_y, score, high_score, game_over, velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp, ground_speed

        
        movement_pp += 2

    while len(pipes) >= 2 and pipes[0].x < -pipes_w:
        pipes.pop(0)
        pipes.pop(0)

    return velocity_y, score, high_score, game_over, velocity_x, gravity, jump_strength, Pipe_Osc_Freq, Pipe_Osc_Amp, ground_speed


# Function to create a pair of pipes (top and bottom)
def create_pp(pipes, top_img, bot_img):
    random_pp_y = pipes_y - pipes_h / 4 - random.random() * (pipes_h / 2)
    phase_offset = random.uniform(0, math.pi * 2)

    top_pp = Pipe(top_img, phase_offset)
    top_pp.y = random_pp_y
    top_pp.base_y = top_pp.y
    pipes.append(top_pp)

    bot_pp = Pipe(bot_img, phase_offset)
    bot_pp.y = top_pp.y + top_pp.h + Opening_Space
    bot_pp.base_y = bot_pp.y
    pipes.append(bot_pp)
