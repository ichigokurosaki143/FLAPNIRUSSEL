import pygame
from sys import exit
import random
 

#ito yung sa panel
Game_Width = 360
Game_Height = 640
 
#RusselDBird
b_x = Game_Width/8
b_y = Game_Height/2
b_w = 34 #naging 17/12 yung ratio kasi yung original ratio ng image ay 408x288
b_h = 24
 
#mga tobo
pp_x = Game_Width
pp_y = 0
pp_w = 64  
pp_h = 512
 

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, b_x, b_y, b_w, b_h)
        self.img = img
 

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pp_x, pp_y, pp_w, pp_h)
        self.img = img
        self.passed = False
 
 
#Backgrund
bg_img = pygame.image.load("flappybirdbg.png")
#Sa ebon
brd_img = pygame.image.load("flappybird.png")
brd_img = pygame.transform.scale(brd_img, (b_w, b_h))
#mga toboh
top_pp_image = pygame.image.load("toppipe.png")
top_pp_image = pygame.transform.scale(top_pp_image, (pp_w, pp_h))
bot_pp_image = pygame.image.load("bottompipe.png")
bot_pp_image = pygame.transform.scale(bot_pp_image, (pp_w, pp_h))
 
#logic ng game
bird = Bird(brd_img)
pipes = []
velocity_x = -2 #beles kung pano gagalaw mga tobo pa kalewa
velocity_y = 0 #move bird up n down speed
gravity = 0.4
score = 0 
game_over = False
 
def draw():
    window.blit(bg_img, (0, 0))
    window.blit(bird.img, bird)
    for pipe in pipes:
        window.blit(pipe.img, pipe)
 
    text_str = str (int(score))
    if game_over:
        text_str = "Game Over:" + text_str
 
    text_font = pygame.font.SysFont("Comic Sams Ms", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))
 
def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)
 
    if bird.y > Game_Height:
        game_over = True
        return
 
 
    for pipe in pipes:
        pipe.x += velocity_x    
 
        if not pipe.passed and bird.x > pipe.x + pp_w:
            score += 0.5 #0.5 kase merong 2 pipes, 0.5*2 = 1, 1 per set of pipes
            pipe.passed = True
 
        if bird.colliderect(pipe):
            game_over = True
            return    

 
    while len(pipes) > 0 and pipes [0].x < -pp_w:
        pipes.pop(0) # removes first element from the list       
 
#sa tobo(pipes)
def create_pp():
    random_pp_y = pp_y - pp_h/4 - random.random()*(pp_h/2) #0-h/2
    opening_space = Game_Height/4
 
    top_pp =  Pipe(top_pp_image)
    top_pp.y = random_pp_y
    pipes.append(top_pp)
 
    bot_pp = Pipe(bot_pp_image)
    bot_pp.y = top_pp.y + top_pp.h + opening_space
    pipes.append(bot_pp)
 
    print(len(pipes))
 

pygame.init()
window = pygame.display.set_mode((Game_Width, Game_Height))
pygame.display.set_caption("Russel In The Wonderland")
clock = pygame.time.Clock()
 
create_pp_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pp_timer, 1625) #marks every secs
 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
 
        if event.type == create_pp_timer and not game_over:
            create_pp()
 
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                velocity_y = -6     
 
                if game_over:
                    bird.y = b_y
                    pipes.clear()
                    score = 0
                    game_over = False
 

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60) #FPS