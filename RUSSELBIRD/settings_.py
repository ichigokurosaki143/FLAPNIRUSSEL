#settings.py

import pygame


# GAME DIMENSION 
Game_Width = 360
Game_Height = 640

# Butas ng Pipes (mas maliit, mas hirap)
Opening_Space = Game_Height / 5.2  # inadjust ko dati 1/4, ngayon mas maliit 

# Base oscillation settings (Ito yung nag papagalaw sa pipes sa pag taas at pag baba)
Pipe_Osc_Amp = 30 # taas baba
Pipe_Osc_Freq = 0.002 # bilis ng taas baba

# BIRD DIMENSION
bird_x = Game_Width / 8
bird_y = Game_Height / 2
bird_w = 34
bird_h = 24

# PIPE DIMENSION
pipes_x = Game_Width
pipes_y = 0
pipes_w = 64
pipes_h = 512