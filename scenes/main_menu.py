import pygame
import pygame.gfxdraw

import config
from engine import events
from engine.menu import MainMenu
from space import SpaceScene


# Создаем игру и окно
pygame.init()
pygame.mixer.init()

# Создаем окно с текущим разрешением
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

pygame.display.set_caption("Space snake")
icon = pygame.image.load('../images/snake_icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

background = pygame.image.load('../images/main_menu/background/galaxy-space.jpg').convert()

main_menu = MainMenu()
main_menu.margin_left = 20
main_menu.margin_top = 10

transparent_box = pygame.Surface((500, 400), pygame.SRCALPHA)
transparent_box.fill((0, 0, 0, 128))
box_pos = screen.get_rect().bottomleft
box_pos = box_pos[0] + 20, box_pos[1] - 20
transparent_box_rect = transparent_box.get_rect(bottomleft=box_pos)

space_scene = SpaceScene(screen)

# Цикл игры
running = True
while running:
    main_menu.draw(transparent_box, transparent_box_rect)

    screen.blit(background, (0, 0))
    screen.blit(transparent_box, transparent_box_rect)

    # Держим цикл на правильной скорости
    clock.tick(config.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == events.NEW_GAME:
            space_scene.start()

    pygame.display.flip()

pygame.quit()
