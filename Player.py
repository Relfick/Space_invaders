import pygame.sprite
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, keys_pressed):
        if keys_pressed[K_UP]:
            self.rect.move_ip(0, -5)
            if self.rect.top < 0:
                self.rect.top = 0
        if keys_pressed[K_DOWN]:
            self.rect.move_ip(0, 5)
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
        if keys_pressed[K_LEFT]:
            self.rect.move_ip(-5, 0)
            if self.rect.left < 0:
                self.rect.left = 0
        if keys_pressed[K_RIGHT]:
            self.rect.move_ip(5, 0)
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH




