import pygame.sprite
from pygame.locals import (
    RLEACCEL,
)
SCREEN_WIDTH = 800


class Explosion(pygame.sprite.Sprite):
    def __init__(self, explosion_rect):
        super(Explosion, self).__init__()
        self.image = pygame.image.load("img/explosion.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(
            center=explosion_rect.center
        )
        self.explosion_center_left = self.rect.left

    def update(self):
        self.rect.move_ip(-10, 0)
        alpha = self.image.get_alpha() - 10
        if alpha <= 0 or self.rect.right < 0:
            self.kill()
        else:
            self.image.set_alpha(alpha)
