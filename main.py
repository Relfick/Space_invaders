import pygame
from Player import Player
from Enemy import Enemy
from Cloud import Cloud
from Weapon import Weapon
from Explosion import Explosion

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text = "Score: " + text
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midright = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    screen.fill((135, 206, 251))
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              SCREEN_WIDTH / 4 * 3, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, SCREEN_WIDTH / 4 * 3, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.time.wait(1000)
    pygame.event.clear()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

score = 0
player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
weapons = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
game_over = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        score = 0
        player = Player()
        enemies = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        weapons = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
    game_over = False

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

    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, SCREEN_WIDTH - 30, 30)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        game_over = True

    for enemy in enemies:
        collided = pygame.sprite.groupcollide(weapons, enemies, True, True)
        if type(collided) == dict:
            for collided_weapon, _ in collided.items():
                explosion = Explosion(collided_weapon.rect)
                explosions.add(explosion)
                all_sprites.add(explosion)
                score += 1
                if score % 5 == 0:
                    Enemy.additional_speed += 3

    pygame.display.flip()
    clock.tick(60)
