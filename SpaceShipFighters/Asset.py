from dataclasses import dataclass, field
import os
from typing import Optional

import pygame


@dataclass
class Asset:
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
        self.image = pygame.image.load(os.path.join("Assets", url))
        return self.image

    def rotate(self, angle: float):
        self.image = pygame.transform.rotate(self.image, angle)
        return self.image

    def adjust_size(self, width: int, height: int):
        self.image = pygame.transform.scale(self.image, (width, height))
        return self.image
