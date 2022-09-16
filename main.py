from dataclasses import dataclass, field
import os
from turtle import width
from typing import Sequence, Optional
import pygame

pygame.font.init()
pygame.mixer.init()

@dataclass
class GameSetting():
    # Overall Game Settings:
    screen_width: int = 900
    screen_heigth: int = 500
    fps: int = 60
    # General Player Settings:
    spaceship_width: int = 55
    spaceship_height: int = 40
    player_max_health: int = 10
    max_bullets: int = 3
    ship_velocity: int = 5
    bullet_velocity: int = 7

    def defind_screen(self) -> pygame.Surface:
        return pygame.display.set_mode((self.screen_width, self.screen_heigth))

@dataclass
class Player():    
    bullets: list[pygame.Rect] = []
    width: Optional[int] = None
    height: Optional[int] = None
    _surface: pygame.Surface = field(init=False, repr=False)
    _health: int = field(init=False, repr=False)
    _image_asset: pygame.Surface = field(init=False, repr=False)

    def __post_init__(self, game_setting: GameSetting, image_asset_path: str,  x: int, y: int) -> None:
        """Sets the username for the user"""
        self._health: int = game_setting.player_max_health
        self.width = self.width if self.width != None else game_setting.spaceship_width
        self.height = self.height if self.height != None else game_setting.spaceship_height
        self._surface: pygame.Surface = pygame.Rect(x, y, self.width, self.height)
        self._image_asset: pygame.Surface = self.adjust_size(self.asign_image_asset(image_asset_path), (self.width, self.height))
    
    def x(self):
        return self._surface.x

    def y(self):
        return self._surface.y

    def asign_image_asset(self, url: str) -> None:
        self._image_asset = pygame.image.load(os.path.join('Assets', url))

    def rotate(self, angle: float):
        self._image_asset = pygame.transform.rotate(self._image_asset, angle)

    def adjust_size(self, width: int, height: int):
        self._image_asset = pygame.transform.scale(self._image_asset, width, height)

    def handle_movement(self, keys_pressed: Sequence[bool]):
        if keys_pressed[pygame.K_a] and self._surface.x - VEL > 0: #LEFT
            self._surface.x -= VEL
        if keys_pressed[pygame.K_d] and self._surface.x + VEL + self._surface.width < BORDER.x: #RIGHT
            self._surface.x += VEL
        if keys_pressed[pygame.K_w] and self._surface.y - VEL > 0: #UP
            self._surface.y -= VEL
        if keys_pressed[pygame.K_s] and self._surface.y + VEL + self._surface.height < HEIGHT - 15: #DOWN
            self._surface.y += VEL



# GAME SETTINGS:
WIDTH: int = 900
HEIGHT: int = 500
FPS: int = 60

# PLAYER SETTINGS:
SPACESHIP_WIDTH: int = 55
SPACESHIP_HEIGHT: int = 40
VEL: int = 5
BULLET_VEL: int = 7
MAX_BULLETS: int = 3
PLAYER_MAX_HEALTH: int = 10

WIN: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))

# WINDOWS SETTINGS:
pygame.display.set_caption("First Game!")
BORDER: pygame.Rect = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNNER_FONT = pygame.font.SysFont('comicsans', 100)

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
BULLET_HIT_SOUND: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# COLORS: Make this into a class
WHITE: tuple = (255,255,255)
BLACK: tuple = (0,0,0)
RED: tuple = (255,0,0)
GREEN: tuple = (0,255,0)
BLUE: tuple = (0,0,255)
YELLOW: tuple = (255,255,0)
MAGENTA: tuple = (255,0,255)
CYAN: tuple = (0,255,255) 
ROYAL_BLUE: tuple = (00,23,66)

def draw_window(red: pygame.Rect, yellow: pygame.Rect, red_bullets: list, yellow_bullets: list, red_health: int, yellow_health: int) -> None:
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

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

def draw_winner(text):
    draw_text = WINNNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))  
    pygame.display.update()
    pygame.time.delay(5000)

def main() -> None:
    """Main game loop"""
    yellow: pygame.Rect = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red: pygame.Rect = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets: list = []
    red_bullets: list = []
    yellow_health: int = PLAYER_MAX_HEALTH
    red_health: int = PLAYER_MAX_HEALTH

    clock: pygame.time.Clock = pygame.time.Clock()
    run: bool = True
    while run:
        clock.tick(FPS)
        event: pygame.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10 ,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_9 and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Yellow Wins!"

        if red_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

                    
        print(yellow_bullets, red_bullets)
        keys_pressed: Sequence[bool] = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Draw items to the window   
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)   
    main()

if __name__ == '__main__':
    main()