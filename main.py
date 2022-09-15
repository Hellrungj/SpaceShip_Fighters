from asyncio import Handle
import os
import turtle
from typing import Sequence
import pygame

# GAME SETTINGS:
WIDTH: int = 900
HEIGHT: int = 500
FPS: int = 60

#PLAYER SETTINGS:
SPACESHIP_WIDTH: int = 55
SPACESHIP_HEIGHT: int = 40
VEL: int = 5
BULLET_VEL: int = 7
MAX_BULLETS: int = 3

WIN: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))

# WINDOWS SETTINGS:
pygame.display.set_caption("First Game!")
BORDER: pygame.Rect = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# User Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# ASSETS:
    # IMAGES:
SPACE: pygame.Surface =  pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

RED_SPACESHP_IMAGE: pygame.Surface = pygame.image.load(os.path.join('Assets', 'spaceship_RED.png'))
RED_SPACESHIP: pygame.Surface = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

YELLOW_SPACESHP_IMAGE: pygame.Surface = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP: pygame.Surface = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

    # AUDIO:

# COLORS: Make this into a class
WHITE: tuple = (255,255,255)
BLACK: tuple = (0,0,0)
RED: turtle = (255,0,0)
YELLOW: tuple = (255,255,0)
ROYAL_BLUE: tuple = (00,23,66)

def draw_window(red: pygame.Rect, yellow: pygame.Rect, red_bullets: list, yellow_bullets: list) -> None:
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        

    pygame.display.update()

def yellow_handle_movement(keys_pressed: Sequence[bool], yellow: pygame.Rect):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #DOWN
        yellow.y += VEL
        
def red_handle_movement(keys_pressed: Sequence[bool], red: pygame.Rect) -> None:
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        

def main() -> None:
    """Main game loop"""
    yellow: pygame.Rect = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red: pygame.Rect = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets: list = []
    red_bullets: list = []

    clock: pygame.time.Clock = pygame.time.Clock()
    run: bool = True
    while run:
        clock.tick(FPS)
        event: pygame.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10 ,5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_9 and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    
        print(yellow_bullets, red_bullets)
        keys_pressed: Sequence[bool] = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Draw items to the window   
        draw_window(red, yellow, red_bullets, yellow_bullets)   
    pygame.quit()

if __name__ == '__main__':
    main()