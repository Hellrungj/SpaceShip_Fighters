import os
import pygame
from typing import Any, Sequence

from SpaceShipFighters.GameSetting import GameSetting
from SpaceShipFighters.Player import Player
from SpaceShipFighters.Screen import Screen

pygame.font.init()
pygame.mixer.init()

# # AUDIO:
# BULLET_HIT_SOUND: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
# BULLET_FIRE_SOUND: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

# User Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# FONT
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNNER_FONT = pygame.font.SysFont("comicsans", 100)


def handle_movement(player: Player, keys_pressed: Sequence[bool], screen: Screen):
    if player.side == 0:  # LEFT SIDE
        if (
            keys_pressed[player.controls["LEFT"]]
            and player.surface.x - player.movement_velocity > 0
        ):  # LEFT
            player.surface.x -= player.movement_velocity
        if (
            keys_pressed[player.controls["RIGHT"]]
            and player.surface.x + player.movement_velocity + player.surface.width
            < screen.border.x
        ):  # RIGHT
            player.surface.x += player.movement_velocity
    else:  # RIGHT SIDE
        if (
            keys_pressed[player.controls["LEFT"]]
            and player.surface.x - player.movement_velocity
            > screen.border.x + screen.border.width
        ):  # LEFT
            player.surface.x -= player.movement_velocity
        if (
            keys_pressed[player.controls["RIGHT"]]
            and player.surface.x + player.movement_velocity + player.width
            < screen.width
        ):  # RIGHT
            player.surface.x += player.movement_velocity
    if (
        keys_pressed[player.controls["UP"]]
        and player.surface.y - player.movement_velocity > 0
    ):  # UP
        player.surface.y -= player.movement_velocity
    if (
        keys_pressed[player.controls["DOWN"]]
        and player.surface.y + player.movement_velocity + player.surface.height
        < screen.height - 15
    ):  # DOWN
        player.surface.y += player.movement_velocity

def draw_window(screen: Screen, player1: Player, player2: Player) -> None:
    screen.surface.blit(screen.background, (0, 0))
    pygame.draw.rect(screen.surface, (0, 0, 0), screen.border)

    yellow_health_text = HEALTH_FONT.render(
        f"Health: {player1.health}", 1, (255, 255, 255)
    )
    red_health_text = HEALTH_FONT.render(
        f"Health: {player2.health}", 1, (255, 255, 255)
    )
    screen.surface.blit(yellow_health_text, (10, 10))
    screen.surface.blit(
        red_health_text, (screen.width - red_health_text.get_width() - 10, 10)
    )

    screen.surface.blit(player1.image_asset, (player1.x, player1.y))
    screen.surface.blit(player2.image_asset, (player2.x, player2.y))

    for bullet in player1.bullets:
        pygame.draw.rect(screen.surface, (255, 255, 0), bullet.surface)

    for bullet in player2.bullets:
        pygame.draw.rect(screen.surface, (255, 0, 0), bullet.surface)

    pygame.display.update()


def handle_bullets(player1: Player, player2: Player, screen: Screen):
    for bullet in player1.bullets:
        bullet.surface.x += 7
        if player2.surface.colliderect(bullet.surface):
            pygame.event.post(pygame.event.Event(RED_HIT))
            player1.bullets.remove(bullet)
        elif bullet.surface.x > screen.width:
            player1.bullets.remove(bullet)

    for bullet in player2.bullets:
        bullet.surface.x -= 7
        if player1.surface.colliderect(bullet.surface):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            player2.bullets.remove(bullet)
        elif bullet.surface.x < 0:
            player2.bullets.remove(bullet)

def handle_bullet_fire(player1: Player, player2: Player, event: Any, settings: GameSetting, bullet_fire_sound: pygame.mixer.Sound):
    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_1 and len(player1.bullets) < settings.max_bullets):
            coordinate: tuple = (player1.x + player1.width, player1.y + player1.height // 2 - 2, 10, 5)
            player1.add_bullet(coordinate, settings.bullet_velocity)
            bullet_fire_sound.play()

        if (event.key == pygame.K_9 and len(player2.bullets) < settings.max_bullets):
            coordinate: tuple = (player2.x, player2.y + player2.height // 2 - 2, 10, 5)
            player2.add_bullet(coordinate, settings.bullet_velocity)
            bullet_fire_sound.play()

def handle_hit(event: Any, player1: Player, player2: Player, bullet_hit_sound: pygame.mixer.Sound):
    if event.type == YELLOW_HIT:
        player1.health -= 1
        bullet_hit_sound.play()

    if event.type == RED_HIT:
        player2.health -= 1
        bullet_hit_sound.play()

def draw_winner(text: str, screen: Screen):
    draw_text = WINNNER_FONT.render(text, 1, (255, 255, 255))
    screen.surface.blit(
        draw_text,
        (
            screen.width // 2 - draw_text.get_width() // 2,
            screen.height // 2 - draw_text.get_height() // 2,
        ),
    )
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
            "FIRE": pygame.K_f,
        },
        {
            "LEFT": pygame.K_LEFT,
            "RIGHT": pygame.K_RIGHT,
            "UP": pygame.K_UP,
            "DOWN": pygame.K_DOWN,
            "FIRE": pygame.K_SLASH,
        },
    ]
    settings: GameSetting = GameSetting()
    screen: Screen = Screen(settings=settings)

    # Background IMAGE
    screen.background: pygame.Surface = pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "space.png")),
        (screen.width, screen.height),
    )

    player1: Player = Player(
        controls=player_controls[0],
        side=0,
        settings=settings,
        image_asset_path="spaceship_yellow.png",
        x=100,
        y=300,
        angle=90,
    )
    player2: Player = Player(
        controls=player_controls[1],
        side=1,
        settings=settings,
        image_asset_path="spaceship_red.png",
        x=700,
        y=300,
        angle=270,
    )

    # AUDIO:
    bullet_hit_sound: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
    bullet_fire_sound: pygame.mixer.Sound = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

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

            handle_bullet_fire(player1, player2, event, settings, bullet_fire_sound)
            handle_hit(event, player1, player2, bullet_hit_sound)

        winner_text = ""
        if player1.health <= 0:
            winner_text = "Player 2 Wins!"

        if player2.health <= 0:
            winner_text = "Player 1 Wins!"

        if winner_text != "":
            draw_winner(winner_text, screen)
            break

        keys_pressed: Sequence[bool] = pygame.key.get_pressed()
        handle_movement(player1, keys_pressed, screen)
        handle_movement(player2, keys_pressed, screen)

        handle_bullets(player1, player2, screen)
        print(player1.bullets, player2.bullets)
        draw_window(screen, player1, player2)
    main()


if __name__ == "__main__":
    main()
