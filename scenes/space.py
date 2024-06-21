import pygame
import pymunk
import pymunk.pygame_util

import config
from text import get_text_surface
from engine import ships, space, events


class SpaceLoop:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = space.SpaceBG(screen)
        self.physical_space = space.PhysicalSpace()
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)

        # звуки
        self.bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')
        self.bg_sound.set_volume(config.BG_SOUND)
        self.bg_sound.play()

        self.screen_center = config.WIDTH // 2, config.HEIGHT // 2

    @staticmethod
    def handle_zoom(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and config.ZOOM < 1.6:  # колесико вверх
                config.ZOOM *= 1.1
            elif event.button == 5 and config.ZOOM > 0.55:  # колесико вниз
                config.ZOOM /= 1.1

    def get_loop(self):

        player_ship = ships.Cruiser(self.screen_center)

        space_objects = [
            space.Meteorite((0, 100)),
            space.Meteorite((200, 100)),
            space.Meteorite((config.WIDTH, config.HEIGHT))
        ]

        self.physical_space.add(player_ship)
        for obj in space_objects:
            self.physical_space.add(obj)

        # Цикл игры
        while self.running:

            camera_offset = pymunk.Vec2d(self.screen_center[0] - player_ship.body.position.x,
                                         self.screen_center[1] - player_ship.body.position.y)
            self.physical_space.move_camera(camera_offset)
            self.background.move_camera(camera_offset)

            keys = pygame.key.get_pressed()

            player_ship.inactivity_animation()

            # движение по нажатию на кнопку W
            if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
                player_ship.accelerator_animation()
                player_ship.move_ship()
                player_ship.draw(self.screen)

                # ускорение
                if keys[pygame.K_LALT]:
                    pass

            elif keys[pygame.K_SPACE]:
                player_ship.deceleration_ship()

            # Рисуем корабль
            player_ship.rotate_animation()
            player_ship.draw(self.screen)

            for obj in space_objects:
                obj.draw(self.screen)

            text = f'{player_ship.health}'
            self.screen.blit(get_text_surface(text), (100, 100))

            # Держим цикл на правильной скорости
            self.clock.tick(config.FPS)
            # Ввод процесса (события)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == events.GAME_OVER_EVENT:
                    self.running = False
                elif event.type == events.OBJECT_DESTRUCTION_EVENT:
                    if event.object in space_objects:
                        self.physical_space.remove(event.object)
                        space_objects.remove(event.object)

            # Отрисовка объектов Pymunk
            # physical_space.space.debug_draw(draw_options)
            # после отрисовки всего, обновляем экран

            self.physical_space.get_simulation_step()
            pygame.display.flip()

        pygame.quit()
