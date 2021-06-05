import pygame
from player import Player
from enemy import Enemy
from cloud import Cloud
from bullet import Bullet
from explosion import Explosion
import time
import random


class Game:
    def __init__(self):
        self.score = 0
        self.players = pygame.sprite.Group()
        self.players_num = 25
        for _ in range(self.players_num):
            self.players.add(Player())
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        for player in self.players:
            self.all_sprites.add(player)
        Enemy.additional_speed = 0
        self.max_num_enemies = 6
        self.start_time = time.perf_counter()

    def shoot(self):
        new_weapon = Bullet(self.player.rect)
        self.bullets.add(new_weapon)
        self.all_sprites.add(new_weapon)

    def spawn_enemy(self):
        if self.enemies.__len__() < self.max_num_enemies:
            rand_player = random.randint(0, self.players.__len__()-1)
            i = 0
            for player in self.players:
                if i == rand_player:
                    new_enemy = Enemy(player.rect.center[1])
                    break
                i += 1
            # new_enemy = Enemy()
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)

    def spawn_cloud(self):
        new_cloud = Cloud()
        self.clouds.add(new_cloud)
        self.all_sprites.add(new_cloud)

    def update(self):
        self.enemies.update()
        self.clouds.update()
        self.bullets.update()
        self.explosions.update()

    # def update_player(self, player, pressed_keys):
    #     player.update(pressed_keys)

    def get_all_sprites(self):
        return self.all_sprites

    def get_score(self):
        return self.score

    def get_players(self):
        return self.players

    def get_max_num_enemies(self):
        return self.max_num_enemies

    # def kill_player(self):
    #     self.player.kill()

    def player_collide_enemy(self):
        # pygame.sprite.groupcollide(self.players, self.enemies, True, True)
        # if self.players.__len__() == 0:
        #     return True
        # return False
        for player in self.players:
            if pygame.sprite.spritecollideany(player, self.enemies):
                player.set_time_lived(time.perf_counter() - self.start_time)
                player.kill()
                self.score += 1

        if self.players.__len__() == 0:
            return True
        return False

    def bullet_collide_enemy(self):
        for _ in self.enemies:
            collided = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
            if type(collided) == dict:
                for collided_bullet, _ in collided.items():
                    explosion = Explosion(collided_bullet.rect)
                    self.explosions.add(explosion)
                    self.all_sprites.add(explosion)
                    self.score += 1
                    if self.score % 5 == 0:
                        Enemy.additional_speed += 3

    def get_enemies_centers(self):
        return [x.rect.center for x in self.enemies]


