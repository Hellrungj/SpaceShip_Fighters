from dataclasses import dataclass, field

import pygame
import json
import os


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
    player_controls: dict[str, int] = field(init=False, default_factory=dict)

    def defind_screen(self) -> pygame.Surface:
        return pygame.display.set_mode((self.screen_width, self.screen_heigth))

    def load_settings(self, path: str) -> None:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, path)
        with open(file_path, 'r') as f:
            data = json.load(f)
            print(data)
            self.screen_width = data['screen']['width']
            self.screen_heigth = data['screen']['width']
            self.fps = data['general']['fps']
            self.spaceship_width = data['spaceship']['width']
            self.spaceship_height = data['spaceship']['hieght']
            self.player_max_health = data['spaceship']['max_health']
            self.max_bullets = data['spaceship']['max_bullet']    
            self.ship_velocity = data['spaceship']['movement_velocity']    
            self.bullet_velocity = data['spaceship']['bullet_velocity']   
            self.player_controls = data['contorls']

def main() -> None:
    g = GameSetting()
    g.load_settings('../env/env.dev.json')
    print(g)

if __name__ == "__main__":
    main()