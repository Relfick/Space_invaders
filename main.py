import pygame
from game import Game
from aibot import Bot
from genetic import Genetic
import torch
import numpy as np
from matplotlib import pyplot as plt

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
font_name = pygame.font.match_font('arial')
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
best_times = []
last_average = 0
escalate_mutations = False
reset_mutations = False


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
    secs_to_wait = 1
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
    # waiting = True
    # while waiting:
    #     clock.tick(60)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #         if event.type == pygame.KEYUP:
    #             waiting = False


def process_input_data():
    enemies_centers = game.get_enemies_centers()

    # количество созданных врагов не всегда равно max_num_enemies
    if len(enemies_centers) < max_num_enemies:
        while len(enemies_centers) < max_num_enemies:
            enemies_centers.append((-100, -100))

    player_center = bot.player.rect.center
    player_center = [player_center[0], player_center[1]]
    player_center_y = [player_center[0]]

    # x_data: [x1, y1, x2, y2, ..., x_n_enemies, y_n_enemies]
    # x_data = [item for t in enemies_centers for item in t]

    # x_data: [x1-сx, x2-сx, ..., x_n_enemies-сx, y1-сy, y2-сy, ..., y_n_enemies-сy]
    x_coords = [item[0] - player_center[0] for item in enemies_centers]
    y_coords = [item[1] - player_center[1] for item in enemies_centers]

    # нормализация
    x_coords = list((np.array(x_coords) / SCREEN_WIDTH))
    y_coords = list((np.array(y_coords) / SCREEN_HEIGHT))
    player_center_y = list((np.array(player_center_y) / SCREEN_HEIGHT))
    x_data = x_coords + y_coords
    x_data = player_center_y + x_data
    return x_data


def bot_predict(bot):
    input_data = process_input_data()

    # predictions: [move y ?, move up ? ]
    predictions = bot.predict(torch.Tensor(input_data))

    bot_comms = {
        pygame.K_UP: False, pygame.K_DOWN: False,
        pygame.K_LEFT: False, pygame.K_RIGHT: False
    }
    if predictions[0]:
        bot_comms[pygame.K_UP] = predictions[1]
        bot_comms[pygame.K_DOWN] = not predictions[1]
    return bot_comms


def store_best_time():
    max1, max2 = 0, 0
    for bot in bots:
        lived = bot.player.time_lived
        if lived > max1:
            max2 = max1
            max1 = lived
        elif lived > max2:
            max2 = lived

    print(f"{max1} | {max2}")
    best_times.append((max1 + max2) / 2)


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 400)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

game = Game()
max_num_enemies = game.get_max_num_enemies()
bots = []
for player in game.get_players():
    bots.append(Bot(max_num_enemies, player))

running = True
game_over = False
while running:
    if game_over:
        show_continue_screen()
        store_best_time()
        game_over = False

        if len(best_times) % 10 == 1:
            curr_average = sum(best_times[-10:]) / 10
            if curr_average - last_average < 2:
                escalate_mutations = True
                reset_mutations = False
            else:
                reset_mutations = True
            last_average = curr_average

            plt.plot(best_times)
            plt.show()

        bots = Genetic(bots, escalate_mutations, reset_mutations).get_bots()
        escalate_mutations = False

        game = Game()
        players = game.get_players()
        i = 0
        for player in players:
            bots[i].set_player(player)
            i += 1
        # bots = []
        # for player in game.get_players():
        #     bots.append(Bot(player, max_num_enemies))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                plt.plot(best_times)
                plt.show()

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
    clock.tick(240)
