import pygame

import config
from text import get_text_surface


# Создаем игру и окно
pygame.init()
pygame.mixer.init()

# Создаем окно с текущим разрешением
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

pygame.display.set_caption("Space snake")
icon = pygame.image.load('images/snake_icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Цикл игры
running = True
while running:

    text = f'some'
    screen.blit(get_text_surface(text), (100, 100))

    # Держим цикл на правильной скорости
    clock.tick(config.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
