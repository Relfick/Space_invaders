import pygame.sprite
from pygame.locals import (
    RLEACCEL,
)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, exlposion_rect):
        super(Explosion, self).__init__()
        self.surf = pygame.image.load("explosion.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=exlposion_rect.center
        )

    def update(self):
        self.rect.move_ip(-10, 0)
        if self.rect.right < 0:
            self.kill()
