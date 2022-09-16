from dataclasses import InitVar, dataclass, field
from decimal import Overflow
import os
from turtle import width
from typing import Sequence, Optional, overload
from unittest.mock import seal
from webbrowser import BackgroundBrowser
import pygame

pygame.font.init()
pygame.mixer.init()

# AUDIO:
BULLET_HIT_SOUND: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# User Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#FONT
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNNER_FONT = pygame.font.SysFont('comicsans', 100)

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
    player_controls: list[dict[ str, int]] = field(init=False, default_factory=dict)

    def defind_screen(self) -> pygame.Surface:
        return pygame.display.set_mode((self.screen_width, self.screen_heigth))

@dataclass
class Screen():
    settings: InitVar[GameSetting]
    width: Optional[int] = None
    height: Optional[int] = None
    surface: pygame.Surface = field(init=False)
    border: pygame.Surface = field(init=False)
    background: pygame.Surface = None

    def __post_init__(self, settings: GameSetting):
        if self.width == None and self.width == None:
            self.surface: pygame.Surface = settings.defind_screen()
            self.width = settings.screen_width
            self.height = settings.screen_heigth
        else: 
            self.surface: pygame.Surface = pygame.display.set_mode((self.width, self.heigth))
        self.border: pygame.Rect = pygame.Rect(settings.screen_width // 2 - 5, 0, 10, settings.screen_heigth)

@dataclass
class Asset():
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    angle: Optional[float] = 0
    image: pygame.Surface = field(init=False)

    def __post_init__(self) -> None:
        self.image: pygame.Surface = self.load(self.url)
        self.width = self.width if self.width != None else self.image.get_width()
        self.height = self.height if self.height != None else self.image.get_height()
        self.adjust_size(self.width, self.height)
        self.rotate(self.angle)

    def load(self, url: str) -> None:
        self.image = pygame.image.load(os.path.join('Assets', url))
        return self.image

    def rotate(self, angle: float):
        self.image = pygame.transform.rotate(self.image, angle)
        return self.image

    def adjust_size(self, width: int, height: int):
        self.image = pygame.transform.scale(self.image, (width, height))
        return self.image

@dataclass
class Player():
    controls: dict[str, int]
    side: int
    settings: InitVar[GameSetting]
    image_asset_path: InitVar[Asset]
    x: InitVar[int]
    y: InitVar[int]
    angle: Optional[float] = 0
    bullets: list[pygame.Rect] = field(init=False, default_factory=list)
    width: Optional[int] = None
    height: Optional[int] = None
    health: int = field(init=False)
    surface: pygame.Surface = field(init=False, repr=False)
    health: int = field(init=False, repr=False)
    image_asset: pygame.Surface = field(init=False, repr=False)
    movement_velocity: int = field(init=False, repr=False)

    def __post_init__(self, settings: GameSetting, image_asset_path: str,  x: int, y: int) -> None:
        """Sets the username for the user"""
        self._health: int = settings.player_max_health
        self.width = self.width if self.width != None else settings.spaceship_width
        self.height = self.height if self.height != None else settings.spaceship_height
        self.health = settings.player_max_health
        self.surface: pygame.Surface = pygame.Rect(x, y, self.width, self.height)
        self.asign_image_asset = Asset(image_asset_path, self.width, self.height, self.angle)
        self.image_asset = self.asign_image_asset.image
        self.movement_velocity = settings.ship_velocity

    @property
    def x(self):
        return self.surface.x

    @property
    def y(self):
        return self.surface.y

def handle_movement(player: Player, keys_pressed: Sequence[bool], screen: Screen):
    if player.side == 0: # LEFT SIDE
        if keys_pressed[player.controls['LEFT']] and player.surface.x - player.movement_velocity > 0: #LEFT
            player.surface.x -= player.movement_velocity
        if keys_pressed[player.controls['RIGHT']] and player.surface.x + player.movement_velocity + player.surface.width < screen.border.x: #RIGHT
            player.surface.x += player.movement_velocity
    else: # RIGHT SIDE
        if keys_pressed[player.controls['LEFT']] and player.surface.x - player.movement_velocity > screen.border.x + screen.border.width: #LEFT
            player.surface.x -= player.movement_velocity
        if keys_pressed[player.controls['RIGHT']] and player.surface.x + player.movement_velocity + player.width < screen.width: #RIGHT
            player.surface.x += player.movement_velocity
    if keys_pressed[player.controls['UP']] and player.surface.y - player.movement_velocity > 0: #UP
        player.surface.y -= player.movement_velocity
    if keys_pressed[player.controls['DOWN']] and player.surface.y + player.movement_velocity + player.surface.height < screen.height - 15: #DOWN
        player.surface.y += player.movement_velocity

def handle_bullet_fire(player: Player, keys_pressed: Sequence[bool], screen: Screen, trager_player: Player):
    ...

def draw_window(screen: Screen, player1: Player, player2: Player) -> None:
    screen.surface.blit(screen.background, (0,0))
    pygame.draw.rect(screen.surface, (0,0,0), screen.border)

    yellow_health_text = HEALTH_FONT.render(f"Health: {player1.health}", 1, (255,255,255))
    red_health_text = HEALTH_FONT.render(f"Health: {player2.health}", 1, (255,255,255))
    screen.surface.blit(yellow_health_text, (10, 10))
    screen.surface.blit(red_health_text, (screen.width - red_health_text.get_width() - 10, 10))

    screen.surface.blit(player1.image_asset,(player1.x, player1.y))
    screen.surface.blit(player2.image_asset,(player2.x, player2.y))

    for bullet in player1.bullets:
        pygame.draw.rect(screen.surface, (255,255,0), bullet)

    for bullet in player2.bullets:
        pygame.draw.rect(screen.surface, (255,0,0), bullet)

    pygame.display.update()

def handle_bullets(player1: Player, player2: Player, screen: Screen):
    for bullet in player1.bullets:
        bullet.x += 7
        if player2.surface.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            player1.bullets.remove(bullet)
        elif bullet.x > screen.width:
            player1.bullets.remove(bullet)

    for bullet in player2.bullets:
        bullet.x -= 7
        if player1.surface.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            player2.bullets.remove(bullet)
        elif bullet.x < 0:
            player2.bullets.remove(bullet)

def draw_winner(text:str ,screen: Screen):
    draw_text = WINNNER_FONT.render(text, 1, (255,255,255))
    screen.surface.blit(draw_text, (screen.width // 2 - draw_text.get_width() // 2, screen.height // 2 - draw_text.get_height() // 2))  
    pygame.display.update()
    pygame.time.delay(5000)

def main() -> None:
    """Main game loop"""
    player_controls = [ 
        {
            "LEFT": pygame.K_a,
            "RIGHT": pygame.K_d,
            "UP": pygame.K_w,
            "DOWN": pygame.K_s,
            "FIRE": pygame.K_f
        },
        {
            "LEFT": pygame.K_LEFT,
            "RIGHT": pygame.K_RIGHT,
            "UP": pygame.K_UP,
            "DOWN": pygame.K_DOWN,
            "FIRE": pygame.K_SLASH
        },
    ]
    settings: GameSetting = GameSetting()
    screen: Screen = Screen(settings=settings)
    
    # Background IMAGE
    screen.background: pygame.Surface =  pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (screen.width, screen.height))

    player1: Player = Player(controls=player_controls[0],side=0, settings=settings, image_asset_path='spaceship_yellow.png', x=100, y=300, angle=90)
    player2: Player = Player(controls=player_controls[1],side=1,settings=settings, image_asset_path='spaceship_red.png', x=700, y=300, angle=270)

    clock: pygame.time.Clock = pygame.time.Clock()
    run: bool = True
    while run:
        clock.tick(60)
        event: pygame.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(player1.bullets) < settings.max_bullets:
                    bullet = pygame.Rect(player1.x + player1.width, player1.y + player1.height // 2 - 2, 10 ,5)
                    player1.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_9 and len(player2.bullets) < settings.max_bullets:
                    bullet = pygame.Rect(player2.x, player2.y + player2.height // 2 - 2, 10, 5)
                    player2.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                player1.health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                player2.health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if player1.health <= 0:
            winner_text = "Yellow Wins!"

        if player2.health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text, screen)
            break

        keys_pressed: Sequence[bool] = pygame.key.get_pressed()
        handle_movement(player1, keys_pressed, screen)
        handle_movement(player2, keys_pressed, screen)

        handle_bullets(player1, player2, screen)
        draw_window(screen, player1, player2)
    main()

if __name__ == '__main__':
    main()