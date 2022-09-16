from dataclasses import InitVar, dataclass, field
import os
from turtle import width
from typing import Sequence, Optional
from unittest.mock import seal
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

    def __post_init__(self, settings: GameSetting):
        if self.width == None and self.width == None:
            self.surface: pygame.Surface = settings.defind_screen()
            self.width = settings.screen_width
            self.height = settings.screen_heigth
        else: 
            self.surface: pygame.Surface = pygame.display.set_mode((self.width, self.heigth))
        self.border: pygame.Rect = pygame.Rect(settings.screen_width // 2 - 5, 0, 10, settings.screen_heigth)

@dataclass
class Player():
    controls: dict[str, int]
    side: int
    settings: InitVar[GameSetting]
    image_asset_path: InitVar[str]
    x: InitVar[int]
    y: InitVar[int]
    angle: Optional[int] = 0
    bullets: list[pygame.Rect] = field(init=False, default_factory=list)
    width: Optional[int] = None
    height: Optional[int] = None
    health: int = field(init=False)
    _surface: pygame.Surface = field(init=False, repr=False)
    _health: int = field(init=False, repr=False)
    _image_asset: pygame.Surface = field(init=False, repr=False)
    _movement_velocity :int = field(init=False, repr=False)

    def __post_init__(self, settings: GameSetting, image_asset_path: str,  x: int, y: int) -> None:
        """Sets the username for the user"""
        self._health: int = settings.player_max_health
        self.width = self.width if self.width != None else settings.spaceship_width
        self.height = self.height if self.height != None else settings.spaceship_height
        self.health = settings.player_max_health
        self._surface: pygame.Surface = pygame.Rect(x, y, self.width, self.height)
        self.asign_image_asset(image_asset_path)
        self.adjust_size(self.width, self.height)
        self.rotate(self.angle)
        self._movement_velocity = settings.ship_velocity

    @property
    def x(self):
        return self._surface.x

    @property
    def y(self):
        return self._surface.y

    def asign_image_asset(self, url: str) -> None:
        self._image_asset = pygame.image.load(os.path.join('Assets', url))

    def rotate(self, angle: float):
        self._image_asset = pygame.transform.rotate(self._image_asset, angle)

    def adjust_size(self, width: int, height: int):
        self._image_asset = pygame.transform.scale(self._image_asset, (width, height))

    def handle_movement(self, keys_pressed: Sequence[bool], screen: Screen):
        if self.side == 0: # LEFT SIDE
            if keys_pressed[self.controls['LEFT']] and self._surface.x - self._movement_velocity > 0: #LEFT
                self._surface.x -= self._movement_velocity
            if keys_pressed[self.controls['RIGHT']] and self._surface.x + self._movement_velocity + self._surface.width < screen.border.x: #RIGHT
                self._surface.x += self._movement_velocity
        else: # RIGHT SIDE
            if keys_pressed[self.controls['LEFT']] and self._surface.x - self._movement_velocity > screen.border.x + screen.border.width: #LEFT
                self._surface.x -= self._movement_velocity
            if keys_pressed[self.controls['RIGHT']] and self._surface.x + self._movement_velocity + self.width < screen.width: #RIGHT
                self._surface.x += self._movement_velocity
        if keys_pressed[self.controls['UP']] and self._surface.y - self._movement_velocity > 0: #UP
            self._surface.y -= self._movement_velocity
        if keys_pressed[self.controls['DOWN']] and self._surface.y + self._movement_velocity + self._surface.height < screen.height - 15: #DOWN
            self._surface.y += self._movement_velocity

def draw_window(screen: Screen, player1: Player, player2: Player) -> None:
    screen.surface.fill((255,255,255))
    pygame.draw.rect(screen.surface, (0,0,0), screen.border)

    screen.surface.blit(player1._image_asset,(player1.x, player1.y))
    screen.surface.blit(player2._image_asset,(player2.x, player2.y))

    pygame.display.update()

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
    
    player1: Player = Player(controls=player_controls[0],side=0, settings=settings, image_asset_path='spaceship_red.png', x=100, y=300, angle=90)
    player2: Player = Player(controls=player_controls[1],side=1,settings=settings, image_asset_path='spaceship_yellow.png', x=700, y=300, angle=270)


    clock: pygame.time.Clock = pygame.time.Clock()
    run: bool = True
    while run:
        clock.tick(settings.fps)
        event: pygame.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        keys_pressed: Sequence[bool] = pygame.key.get_pressed()
        player1.handle_movement(keys_pressed, screen)
        player2.handle_movement(keys_pressed, screen)
        draw_window(screen, player1, player2)
    pygame.quit()
    exit()

if __name__ == '__main__':
    main()