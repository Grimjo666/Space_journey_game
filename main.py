import pygame
import pymunk
import pymunk.pygame_util

import config
from text import get_text_surface
from engine import ships, space, events

# Создаем игру и окно
pygame.init()
pygame.mixer.init()

# Создаем окно с текущим разрешением
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


screen_center = config.WIDTH // 2, config.HEIGHT // 2
player_ship = ships.Cruiser(screen_center)

space_objects = [
    space.Meteorite((0, 100)),
    space.Meteorite((200, 100)),
    space.Meteorite((config.WIDTH, config.HEIGHT))
]

physical_space.add(player_ship)
for obj in space_objects:
    physical_space.add(obj)


def handle_zoom(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4 and config.ZOOM < 1.6:  # колесико вверх
            config.ZOOM *= 1.1
        elif event.button == 5 and config.ZOOM > 0.55:  # колесико вниз
            config.ZOOM /= 1.1


# Цикл игры
running = True
while running:

    camera_offset = pymunk.Vec2d(screen_center[0] - player_ship.body.position.x,
                                 screen_center[1] - player_ship.body.position.y)
    physical_space.move_camera(camera_offset)
    background.move_camera(camera_offset)

    keys = pygame.key.get_pressed()

    player_ship.inactivity_animation()

    # движение по нажатию на кнопку W
    if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
        player_ship.accelerator_animation()
        player_ship.move_ship()
        player_ship.draw(screen)

        # ускорение
        if keys[pygame.K_LALT]:
            pass

    elif keys[pygame.K_SPACE]:
        player_ship.deceleration_ship()

    # Рисуем корабль
    player_ship.rotate_animation()
    player_ship.draw(screen)

    for obj in space_objects:
        obj.draw(screen)

    text = f'{player_ship.health}'
    screen.blit(get_text_surface(text), (100, 100))

    # Держим цикл на правильной скорости
    clock.tick(config.FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == events.GAME_OVER_EVENT:
            print('sssssssssss')
        elif event.type == events.OBJECT_DESTRUCTION_EVENT:
            if event.object in space_objects:
                physical_space.remove(event.object)
                space_objects.remove(event.object)

    # Отрисовка объектов Pymunk
    # physical_space.space.debug_draw(draw_options)
    # после отрисовки всего, обновляем экран

    physical_space.get_simulation_step()
    pygame.display.flip()

pygame.quit()
