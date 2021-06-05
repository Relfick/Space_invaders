import pygame.sprite
import random
from pygame.locals import (
    RLEACCEL,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Enemy(pygame.sprite.Sprite):
    additional_speed = 0

    def __init__(self, player_y=None):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("img/missile.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        if player_y is None:
            self.rect = self.image.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 50),
                    random.randint(0, SCREEN_HEIGHT)
                )
            )
        else:
            self.rect = self.image.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 50),
                    player_y
                )
            )
        # self.speed = random.randint(5 + self.additional_speed, 10 + self.additional_speed)
        self.speed = 7

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
