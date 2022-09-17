from dataclasses import dataclass

import pygame


@dataclass
class Bullet:
    surface: pygame.Surface
    movement_velocity: int