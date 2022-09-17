from dataclasses import InitVar, dataclass, field
from types import coroutine
from typing import Optional

import pygame

from SpaceShipFighters.Asset import Asset
from SpaceShipFighters.Bullet import Bullet
from SpaceShipFighters.GameSetting import GameSetting


@dataclass
class Player:
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

    def __post_init__(
        self, settings: GameSetting, image_asset_path: str, x: int, y: int
    ) -> None:
        """Sets the username for the user"""
        self._health: int = settings.player_max_health
        self.width = self.width if self.width != None else settings.spaceship_width
        self.height = self.height if self.height != None else settings.spaceship_height
        self.health = settings.player_max_health
        self.surface: pygame.Surface = pygame.Rect(x, y, self.width, self.height)
        self.asign_image_asset = Asset(
            image_asset_path, self.width, self.height, self.angle
        )
        self.image_asset = self.asign_image_asset.image
        self.movement_velocity = settings.ship_velocity

    @property
    def x(self):
        return self.surface.x

    @property
    def y(self):
        return self.surface.y

    def add_bullet(self, coordinate: tuple, bullet_velocity: int) -> Bullet:
        p1,p2,p3,p4 = coordinate
        bullet = Bullet(pygame.Rect(p1,p2,p3,p4), bullet_velocity)
        self.bullets.append(bullet)
        return bullet
