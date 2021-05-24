import pygame.sprite
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
SCREEN_WIDTH = 800


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player_rect: pygame.Rect):
        super(Weapon, self).__init__()
        self.image = pygame.image.load("weapon.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(
            center=player_rect.center
        )
        self.rect.move_ip(30, 0)

    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
