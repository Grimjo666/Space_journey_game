# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import math


import config
from text import get_text_surface
from sprites import *


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
    pygame.image.load('images/player/ship_2/ship_2.png').convert_alpha(),
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


def smooth_rotation(first_angle, second_angle):
    # Логика поворота с симуляцией массы корабля
    difference = second_angle - first_angle
    if difference > 180:
        difference -= 360
    elif difference < -180:
        difference += 360

    # Замедление в конце поворота
    if abs(difference) < config.ROTATE_SLOWDOWN_THRESHOLD:
        rotate_speed = max(config.MIN_ROTATE_SPEED,
                           config.ROTATE_SPEED * abs(difference) // config.ROTATE_SLOWDOWN_THRESHOLD)
    else:
        rotate_speed = config.ROTATE_SPEED

    if difference != 0:

        if abs(difference) < rotate_speed:
            first_angle += difference
        else:
            first_angle += math.copysign(rotate_speed, difference)

    first_angle %= 360
    return first_angle


def calculate_angle(mouse_cord, player_cord):
    m_x, m_y = mouse_cord
    p_x, p_y = player_cord

    result_angle = math.atan2(p_y - m_y, m_x - p_x)

    if result_angle < 0:  # Если угол отрицательный, добавляем 2 * пи
        result_angle += 2 * math.pi

    return result_angle * 180 / math.pi


def get_movement_vector(angle, speed):
    # Преобразование угла из градусов в радианы
    radian_angle = math.radians(angle)

    # Вычисление изменений по осям x и y
    dx = speed * math.cos(radian_angle)
    dy = speed * math.sin(radian_angle)

    return dx, dy


current_angle = None
player_position = screen.get_rect().center

# Цикл игры
running = True
while running:

    keys = pygame.key.get_pressed()

    # координаты мыши/игрока и их относительный угол
    m_cord = list(pygame.mouse.get_pos())
    desired_angle = int(calculate_angle(m_cord, player_position))

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

    player = player_movement[0]
    rotated_player = pygame.transform.rotate(player, current_angle - 90)
    rotated_rect = rotated_player.get_rect(center=player_position)
    screen.blit(rotated_player, rotated_rect.topleft)

    # активируем вращение корабля
    current_angle = smooth_rotation(current_angle, desired_angle)

    # движение по нажатию на кнопку W
    if keys[pygame.K_w]:

        move_x, move_y = get_movement_vector(current_angle, config.MOVE_SPEED)

        if keys[pygame.K_LALT]:
            move_x *= 2
            move_y *= 2

        # if current_angle == desired_angle:
        #     player_position = player_position[0] + move_x, player_position[1] + move_y

        bg_x -= move_x
        bg_y += move_y

    text = f'mouse: {m_cord}, rev_mouse: '
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



