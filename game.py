import pygame
from player import Player
from enemy import Enemy
from cloud import Cloud
from bullet import Bullet
from explosion import Explosion

class Game:
    def __init__(self):
        self.score = 0
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        Enemy.additional_speed = 0

    def shoot(self):
        new_weapon = Bullet(self.player.rect)
        self.bullets.add(new_weapon)
        self.all_sprites.add(new_weapon)

    def spawn_enemy(self):
        new_enemy = Enemy()
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def spawn_cloud(self):
        new_cloud = Cloud()
        self.clouds.add(new_cloud)
        self.all_sprites.add(new_cloud)

    def update(self, pressed_keys):
        self.player.update(pressed_keys)
        self.enemies.update()
        self.clouds.update()
        self.bullets.update()
        self.explosions.update()

    def get_all_sprites(self):
        return self.all_sprites

    def get_score(self):
        return self.score

    def kill_player(self):
        self.player.kill()

    def player_collide_enemy(self):
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player.kill()
            return True
        return False

    def bullet_collide_enemy(self):
        for enemy in self.enemies:
            collided = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
            if type(collided) == dict:
                for collided_bullet, _ in collided.items():
                    explosion = Explosion(collided_bullet.rect)
                    self.explosions.add(explosion)
                    self.all_sprites.add(explosion)
                    self.score += 1
                    if self.score % 5 == 0:
                        Enemy.additional_speed += 3



