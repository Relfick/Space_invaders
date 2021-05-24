import pygame.sprite
from pygame.locals import (
    RLEACCEL,
)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, explosion_rect):
        super(Explosion, self).__init__()
        self.image = pygame.image.load("explosion.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(
            center=explosion_rect.center
        )

    def update(self):
        self.rect.move_ip(-10, 0)
        if self.rect.right < 0:
            self.kill()
