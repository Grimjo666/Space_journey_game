# Pygame шаблон - скелет для нового проекта Pygame
import pygame

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

# спрайты и изображения
meteorite_sprite = pygame.image.load('images/space_objects/meteorites/meteorite_1.png').convert_alpha()

background = space.SpaceBG(screen)

# звуки
bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')

bg_sound.set_volume(config.BG_SOUND)
bg_sound.play()

# переменные анимации движения
stars_bg_y = 0
stars_bg_x = 0

speed_x = speed_y = 0

player_position = screen.get_rect().center
player_ship = ships.Cruiser(player_position)

met_x, met_y = 0, 0


# Цикл игры
running = True
while running:

    keys = pygame.key.get_pressed()

    background.draw_stars_bg(speed_x, speed_y)

    screen.blit(meteorite_sprite, (met_x, met_y))

    player_ship.inactivity_animation()

    # движение по нажатию на кнопку W
    if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
        player_ship.accelerator_animation(screen)

        # вектор движения корабля
        speed_x, speed_y = player_ship.move_ship()

        # ускорение
        if keys[pygame.K_LALT]:
            pass

    elif keys[pygame.K_SPACE]:
        speed_x, speed_y = player_ship.deceleration_ship()

    # Рисуем корабль
    player_ship.rotate_animation(screen)

    met_x -= speed_x
    met_y += speed_y

    text = f'x {stars_bg_x}, y {stars_bg_y} {config.HEIGHT}'
    screen.blit(get_text_surface(text), (100, 100))

    # Держим цикл на правильной скорости
    clock.tick(config.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # после отрисовки всего, обновляем экран
    pygame.display.flip()

pygame.quit()
