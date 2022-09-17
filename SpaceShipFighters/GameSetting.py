from dataclasses import dataclass, field

import pygame


@dataclass
class GameSetting:
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
    player_controls: list[dict[str, int]] = field(init=False, default_factory=dict)

    def defind_screen(self) -> pygame.Surface:
        return pygame.display.set_mode((self.screen_width, self.screen_heigth))

    def load_settings() -> None:
        return NotImplemented
