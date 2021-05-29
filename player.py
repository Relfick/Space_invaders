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
        self.image = pygame.image.load("img/jet.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.flight_mode = 'r'
        self.speed = 5

    def change_image(self, image_name):
        tmp_rect = self.rect.copy()
        self.image = pygame.image.load(image_name).convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=tmp_rect.center
        )

    def update(self, keys_pressed):
        if keys_pressed[K_UP]:
            if keys_pressed[K_RIGHT] or keys_pressed[K_LEFT]:
                if self.flight_mode != 'ru':
                    self.flight_mode = 'ru'
                    self.change_image('img/jetm20.png')
            else:
                if self.flight_mode != 'u':
                    self.flight_mode = 'u'
                    self.change_image('img/jetm40.png')

            self.rect.move_ip(0, -self.speed)
            if self.rect.top < 0:
                self.rect.top = 0

        if keys_pressed[K_DOWN]:
            if keys_pressed[K_RIGHT] or keys_pressed[K_LEFT]:
                if self.flight_mode != 'rd':
                    self.flight_mode = 'rd'
                    self.change_image('img/jet20.png')
            else:
                if self.flight_mode != 'd':
                    self.flight_mode = 'd'
                    self.change_image('img/jet40.png')

            self.rect.move_ip(0, self.speed)
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

        if keys_pressed[K_LEFT]:
            if not keys_pressed[K_DOWN] and not keys_pressed[K_UP]:
                if self.flight_mode != 'r':
                    self.flight_mode = 'r'
                    self.change_image('img/jet.png')

            self.rect.move_ip(-self.speed, 0)
            if self.rect.left < 0:
                self.rect.left = 0

        if keys_pressed[K_RIGHT]:
            if not keys_pressed[K_DOWN] and not keys_pressed[K_UP]:
                if self.flight_mode != 'r':
                    self.flight_mode = 'r'
                    self.change_image('img/jet.png')

            self.rect.move_ip(self.speed, 0)
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

        if sum(keys_pressed) == 0:
            if self.flight_mode != 'r':
                self.flight_mode = 'r'
                self.change_image('img/jet.png')