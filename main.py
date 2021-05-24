import pygame
import random
from Player import Player
from Enemy import Enemy
from Cloud import Cloud
from Weapon import Weapon
from Explosion import Explosion

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
weapons = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                new_weapon = Weapon(player.rect)
                weapons.add(new_weapon)
                all_sprites.add(new_weapon)

        elif event.type == pygame.QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    weapons.update()
    explosions.update()

    screen.fill((135, 206, 251))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    for enemy in enemies:
        collided = pygame.sprite.groupcollide(weapons, enemies, True, True)
        if (type(collided) == dict):
            for collided_weapon, _ in collided.items():
                explosion = Explosion(collided_weapon.rect)
                explosions.add(explosion)
                all_sprites.add(explosion)
        # for killer, killed in collided:
        #     for killed_one in killed:
        #         killed_one.kill()
        #     killer.kill()


    pygame.display.flip()
    clock.tick(60)