import pygame
from game import Game
from aibot import Bot
import torch

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
font_name = pygame.font.match_font('arial')
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midright = (x, y)
    surf.blit(text_surface, text_rect)


def draw_screen(score: str):
    screen.fill((135, 206, 251))
    game.get_all_sprites().draw(screen)
    draw_text(screen, score, 25, SCREEN_WIDTH - 30, 30)


def show_continue_screen():
    secs_to_wait = 2
    for i in range(secs_to_wait):
        screen.fill((135, 206, 251))
        draw_text(screen, "Осталось: " + str(secs_to_wait - i), 22,
                  SCREEN_WIDTH / 4 * 3, SCREEN_HEIGHT / 2)
        pygame.display.flip()
        pygame.time.wait(1000)

    screen.fill((135, 206, 251))
    draw_text(screen, "Press a key to begin", 18, SCREEN_WIDTH / 4 * 3, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.event.clear()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def bot_predict(bot):
    enemies_centers = game.get_enemies_centers()
    if len(enemies_centers) < max_num_enemies:
        while len(enemies_centers) < max_num_enemies:
            enemies_centers.append((-100, -100))

    x_data = [item for t in enemies_centers for item in t]
    player_center = bot.player.rect.center
    player_center = [player_center[0], player_center[1]]
    x_data = player_center + x_data
    predictions = bot.predict(torch.Tensor(x_data))
    bot_comms = {
        pygame.K_RIGHT: False, pygame.K_LEFT: False,
        pygame.K_UP: False, pygame.K_DOWN: False
    }
    if predictions[0]:
        bot_comms[pygame.K_RIGHT] = predictions[2]
        bot_comms[pygame.K_LEFT] = not predictions[2]
    if predictions[1]:
        bot_comms[pygame.K_UP] = predictions[3]
        bot_comms[pygame.K_DOWN] = not predictions[3]
    return bot_comms


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

game = Game()
max_num_enemies = game.get_max_num_enemies()
bots = []
for player in game.get_players():
    bots.append(Bot(player, max_num_enemies))

running = True
game_over = False
while running:
    if game_over:
        show_continue_screen()
        game_over = False
        game = Game()
        bots = []
        for player in game.get_players():
            bots.append(Bot(player, max_num_enemies))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                game.shoot()

        elif event.type == pygame.QUIT:
            running = False

        elif event.type == ADDENEMY:
            game.spawn_enemy()

        elif event.type == ADDCLOUD:
            game.spawn_cloud()

    pressed_keys = pygame.key.get_pressed()

    for bot in bots:
        bot_commands = bot_predict(bot)
        bot.player.update(bot_commands)
    game.update()

    draw_screen('Score: ' + str(game.get_score()))

    if game.player_collide_enemy():
        game_over = True

    game.bullet_collide_enemy()

    pygame.display.flip()
    clock.tick(60)
