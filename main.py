import pygame
import pymunk
import pymunk.pygame_util
import random
import math

import config
from text import get_text_surface
from engine import ships, space

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Space snake")
icon = pygame.image.load('images/snake_icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


# scaled_surface = space.ScaledSurface(config.WIDTH, config.HEIGHT)
background = space.SpaceBG(screen)
physical_space = space.PhysicalSpace()

draw_options = pymunk.pygame_util.DrawOptions(screen)

# звуки
bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')

bg_sound.set_volume(config.BG_SOUND)
bg_sound.play()


screen_center = screen.get_rect().center
player_ship = ships.Cruiser(screen_center)

met_1 = space.Meteorite((0, 0))
met_2 = space.Meteorite((config.WIDTH, 0))
met_3 = space.Meteorite((config.WIDTH, config.HEIGHT))
met_4 = space.Meteorite((0, config.HEIGHT))

physical_space.add(player_ship)
physical_space.add(met_1)
physical_space.add(met_2)
physical_space.add(met_3)
physical_space.add(met_4)


def handle_zoom(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4 and config.ZOOM < 1.6:  # колесико вверх
            config.ZOOM *= 1.1
        elif event.button == 5 and config.ZOOM > 0.55:  # колесико вниз
            config.ZOOM /= 1.1
        # met_1.change_scale()
        # met_2.change_scale()
        # met_3.change_scale()
        # met_4.change_scale()
        # player_ship.change_scale()


# Цикл игры
running = True
while running:

    camera_offset = pymunk.Vec2d(screen_center[0] - player_ship.body.position.x,
                                 screen_center[1] - player_ship.body.position.y) * config.ZOOM
    physical_space.move_camera(camera_offset)
    background.move_camera(camera_offset)

    keys = pygame.key.get_pressed()

    player_ship.inactivity_animation()

    # движение по нажатию на кнопку W
    if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
        player_ship.accelerator_animation()
        player_ship.draw(screen, player_ship.current_sprite)
        # вектор движения корабля
        player_ship.move_ship()

        # ускорение
        if keys[pygame.K_LALT]:
            pass

    elif keys[pygame.K_SPACE]:
        player_ship.deceleration_ship()

    # Рисуем корабль
    player_ship.rotate_animation()
    player_ship.draw(screen, player_ship.current_sprite)

    met_1.draw(screen)
    met_2.draw(screen)
    met_3.draw(screen)
    met_4.draw(screen)

    text = f'текущий ZOOM: {player_ship.body.angle * 180 / math.pi} | {player_ship.move_vector} {player_ship.body.velocity}'
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
    physical_space.space.debug_draw(draw_options)
    # после отрисовки всего, обновляем экран

    physical_space.get_simulation_step()
    pygame.display.flip()

pygame.quit()
