# Pygame шаблон - скелет для нового проекта Pygame
import pygame

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

# звуки
bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')

bg_sound.set_volume(config.BG_SOUND)
bg_sound.play()

# переменные анимации движения
bg_y = 0
bg_x = 0

speed_x = speed_y = 0
x = None

player_move = False
current_angle = None
player_position = screen.get_rect().center

player_ship = ships.Cruiser(player_position)

# Цикл игры
running = True
while running:

    keys = pygame.key.get_pressed()

    # относительный угол
    desired_angle = player_ship.calculate_angle()

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

    player = player_ship.sprite
    rotated_player = pygame.transform.rotate(player, current_angle - 90)
    rotated_rect = rotated_player.get_rect(center=player_position)
    screen.blit(rotated_player, rotated_rect.topleft)

    # активируем вращение корабля
    current_angle = player_ship.smooth_rotation(current_angle, desired_angle)

    if keys[pygame.K_SPACE]:
        speed_x, speed_y = player_ship.deceleration_ship()

    # движение по нажатию на кнопку W
    if keys[pygame.K_w]:

        # вектор движения корабля
        player_ship.get_movement_vector(current_angle)
        speed_x, speed_y = player_ship.move_ship()

        # Добавляем инерцию

        # ускорение
        if keys[pygame.K_LALT]:
            pass

    bg_x -= speed_x
    bg_y += speed_y

    text = f'{keys[pygame.K_w]} x {speed_x} y {speed_y}'
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
