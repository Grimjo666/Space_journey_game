# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import pymunk
import pymunk.pygame_util

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

space_pymunk = pymunk.Space()

draw_options = pymunk.pygame_util.DrawOptions(screen)

# звуки
bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')

bg_sound.set_volume(config.BG_SOUND)
bg_sound.play()


player_position = screen.get_rect().center
player_ship = ships.Cruiser(player_position)

meteorite = space.Meteorite((0, 500))
meteorite_2 = space.Meteorite((1000, 0))

space_pymunk.add(meteorite.body, meteorite.get_circle_shape())
space_pymunk.add(meteorite_2.body, meteorite_2.get_circle_shape())
space_pymunk.add(player_ship.body, player_ship.get_circle_shape())
meteorite.body.velocity = (200, 0)

# Цикл игры
running = True
while running:

    camera_offset = pymunk.Vec2d(player_position[0] - player_ship.body.position.x, player_position[1] - player_ship.body.position.y)
    for body in space_pymunk.bodies:
        body.position += camera_offset

    keys = pygame.key.get_pressed()

    background.draw_stars_bg(*camera_offset)

    meteorite.draw(screen)

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

    text = f'{camera_offset}'
    screen.blit(get_text_surface(text), (100, 100))

    # Держим цикл на правильной скорости
    clock.tick(config.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Отрисовка объектов Pymunk
    space_pymunk.debug_draw(draw_options)
    # после отрисовки всего, обновляем экран
    space_pymunk.step(1 / 30.0)  # Шаг симуляции

    pygame.display.flip()

pygame.quit()
