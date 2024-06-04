# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import math


import config
from text import get_text_surface
from game_objects import ships


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Space snake")
icon = pygame.image.load('images/snake_icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# спрайты и изображения
bg = pygame.image.load('images/background-test.png').convert_alpha()

player_movement = [
    pygame.image.load('images/ship_sprites/ship_2/ship_2.png').convert_alpha(),
]

ship_movement_down = [
    pygame.transform.flip(image, False, True)
    for image in player_movement
]


# звуки
bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')

bg_sound.set_volume(config.BG_SOUND)
bg_sound.play()


# переменные анимации
player_animate_counter = 0
bg_y = 0
bg_x = 0

player_move = False
current_angle = None
player_position = screen.get_rect().center

player_ship = ships.Cruiser(player_position)

# Цикл игры
running = True
while running:

    keys = pygame.key.get_pressed()

    # координаты мыши/игрока и их относительный угол
    m_cord = pygame.mouse.get_pos()
    desired_angle = player_ship.calculate_angle()

    dx = m_cord[0] - player_position[0]
    dy = m_cord[1] - player_position[1]

    screen.blit(bg, (bg_x, bg_y))
    screen.blit(bg, (bg_x, bg_y - config.HEIGHT))
    screen.blit(bg, (bg_x, bg_y + config.HEIGHT))
    screen.blit(bg, (bg_x - config.WIDTH, bg_y))
    screen.blit(bg, (bg_x + config.WIDTH, bg_y))
    screen.blit(bg, (bg_x - config.WIDTH, bg_y - config.HEIGHT))
    screen.blit(bg, (bg_x + config.WIDTH, bg_y + config.HEIGHT))
    screen.blit(bg, (bg_x - config.WIDTH, bg_y + config.HEIGHT))
    screen.blit(bg, (bg_x + config.WIDTH, bg_y - config.HEIGHT))

    # Рисуем корабль
    if current_angle is None or current_angle == desired_angle:
        current_angle = desired_angle

    player = player_ship.SPRITE
    rotated_player = pygame.transform.rotate(player, current_angle - 90)
    rotated_rect = rotated_player.get_rect(center=player_position)
    screen.blit(rotated_player, rotated_rect.topleft)

    # активируем вращение корабля
    current_angle = player_ship.smooth_rotation(current_angle, desired_angle)

    if not keys[pygame.K_w]:

        move_x = 0
        move_y = 0

    # движение по нажатию на кнопку W
    if keys[pygame.K_w]:

        # вектор движения корабля
        move_x, move_y = player_ship.get_movement_vector(current_angle)

        # start_speed_x = move_x / config.MOVE_SPEED
        # move_x = start_speed_x + (move_x - start_speed_x) * 0.2
        # start_speed_x = move_x
        #
        # start_speed_y = move_y / config.MOVE_SPEED
        # move_y = start_speed_y + (move_y - start_speed_y) * 0.2
        # start_speed_y = move_y

        # ускорение
        if keys[pygame.K_LALT]:
            move_x *= 2
            move_y *= 2

    bg_x -= move_x
    bg_y += move_y

    text = f'{keys[pygame.K_w]} x {move_x} y {move_y}'
    screen.blit(get_text_surface(text), (100, 100))

    # Держим цикл на правильной скорости
    clock.tick(config.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # после отрисовки всего, переворачиваем экран
    pygame.display.update()

pygame.quit()



