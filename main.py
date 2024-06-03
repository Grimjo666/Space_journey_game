# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import math


import config
from text import get_text_surface
from sprites import *


print(300 - 200)


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
    pygame.image.load('images/player/base_ship/base-ship.png').convert_alpha(),
    pygame.image.load('images/player/base_ship/base-ship_move_1.png').convert_alpha(),
    pygame.image.load('images/player/base_ship/base-ship_move_2.png').convert_alpha(),
    pygame.image.load('images/player/base_ship/base-ship_move_3.png').convert_alpha()
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

# Вычисляем точку для позиционирования игрока
player_rect = player_movement[0].get_rect()
player_w, player_h = player_rect.size
player_position = ((config.WIDTH / 2) - (player_w / 2), (config.HEIGHT / 2) - (player_h / 2))


def calculate_angle(mouse_cord, player_cord):
    m_x, m_y = mouse_cord
    p_x, p_y = player_cord

    angle = math.atan2(p_y - m_y, m_x - p_x)

    if angle < 0:  # Если угол отрицательный, добавляем 2 * пи
        angle += 2 * math.pi

    return angle * 180 / math.pi


previous_angle = None
player_angel_rotate = list()

# Цикл игры
running = True
while running:

    keys = pygame.key.get_pressed()

    # координаты мыши/игрока и их относительный угол
    m_cord = pygame.mouse.get_pos()
    p_cord = screen.get_rect().center
    angel = int(calculate_angle(m_cord, p_cord))

    dx = m_cord[0] - p_cord[0]
    dy = m_cord[1] - p_cord[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance != 0:
        move_x = (dx / distance) * config.MOVE_SPEED
        move_y = (dy / distance) * config.MOVE_SPEED
    else:
        move_x, move_y = 0, 0

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

    if previous_angle is None or previous_angle == angel:
        previous_angle = angel

    player = player_movement[player_animate_counter]
    rotated_player = pygame.transform.rotate(player, previous_angle - 90)
    screen.blit(rotated_player, player_position)

    if previous_angle < angel:
        previous_angle += math.ceil((angel - previous_angle) / config.ROTATE_SPEED)

    elif previous_angle > angel:
        previous_angle -= math.ceil((previous_angle - angel) / config.ROTATE_SPEED)

    # движение по нажатию на кнопку W
    if keys[pygame.K_w]:

        if keys[pygame.K_LALT]:
            move_x *= 2
            move_y *= 2

        bg_x -= move_x
        bg_y -= move_y

        if player_animate_counter == 3:
            player_animate_counter = 1
        else:
            player_animate_counter += 1
    else:
        player_animate_counter = 0

    text = f'mouse: {m_cord} | ship: {p_cord} | angle: {angel} | prev_angl: {previous_angle} | dife: {(angel - previous_angle)}'
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



