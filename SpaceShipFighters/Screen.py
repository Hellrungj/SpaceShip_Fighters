from dataclasses import InitVar, dataclass, field
from typing import Optional

import pygame

from SpaceShipFighters.GameSetting import GameSetting


@dataclass
class Screen:
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
            self.surface: pygame.Surface = pygame.display.set_mode(
                (self.width, self.heigth)
            )
        self.border: pygame.Rect = pygame.Rect(
            settings.screen_width // 2 - 5, 0, 10, settings.screen_heigth
        )
