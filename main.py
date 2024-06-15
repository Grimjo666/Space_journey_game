import pygame
import pymunk
import pymunk.pygame_util
import random

import config
from text import get_text_surface
from game_objects import ships, space

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Space snake")
icon = pygame.image.load('images/snake_icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


background = space.SpaceBG(screen)
physical_space = space.PhysicalSpace()

draw_options = pymunk.pygame_util.DrawOptions(screen)

# звуки
bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')

bg_sound.set_volume(config.BG_SOUND)
bg_sound.play()


screen_center = screen.get_rect().center
player_ship = ships.Cruiser(screen_center)

x = []

for i in range(10000):
    random_met = space.Meteorite((random.randint(1, 2000), random.randint(1, 2000)))
    x.append(random_met)
    physical_space.add(random_met)

physical_space.add(player_ship)


def handle_zoom(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4 and config.ZOOM < 2:  # колесико вверх
            config.ZOOM *= 1.1
        elif event.button == 5 and config.ZOOM > 0.1:  # колесико вниз
            config.ZOOM /= 1.1


# Цикл игры
running = True
while running:

    camera_offset = pymunk.Vec2d(screen_center[0] - player_ship.body.position.x, screen_center[1] - player_ship.body.position.y) * config.ZOOM
    physical_space.move_camera(camera_offset)
    background.move_camera(camera_offset)

    keys = pygame.key.get_pressed()

    for i in x:
        i.draw(screen)

    player_ship.inactivity_animation()

    # движение по нажатию на кнопку W
    if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
        player_ship.accelerator_animation(screen)

        # вектор движения корабля
        player_ship.move_ship()

        # ускорение
        if keys[pygame.K_LALT]:
            pass

    elif keys[pygame.K_SPACE]:
        player_ship.deceleration_ship()

    # Рисуем корабль
    player_ship.rotate_animation(screen)

    text = f'{config.ZOOM}'
    screen.blit(get_text_surface(text), (100, 100))

    # Держим цикл на правильной скорости
    clock.tick(config.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        handle_zoom(event)

    # Отрисовка объектов Pymunk
    # physical_space.space.debug_draw(draw_options)
    # после отрисовки всего, обновляем экран

    physical_space.get_simulation_step()

    pygame.display.flip()

pygame.quit()
