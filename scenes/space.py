import pygame
import pymunk
import pymunk.pygame_util

import config
from engine import ships, space, events, scene
from engine.camera import Camera


class SpaceScene(scene.BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        self.camera = Camera()

        self.background = space.SpaceBG(screen)
        self.planets = space.SpaceBGPlanets(self.background.surface)
        self.physical_space = space.PhysicalSpace()
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)

        # звуки
        self.bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')
        self.bg_sound.set_volume(config.BG_SOUND)
        self.bg_sound.play()

        self.screen_center = config.WIDTH // 2, config.HEIGHT // 2

        self.player_ship = ships.Cruiser(self.screen_center)

        self.space_objects = None

    def create_objects(self):
        self.space_objects = [
            space.Meteorite((0, 100)),
            space.Meteorite((200, 100)),
            space.Meteorite((config.WIDTH, config.HEIGHT))
        ]

        self.physical_space.add(self.player_ship)
        for obj in self.space_objects:
            self.physical_space.add(obj)

    @staticmethod
    def handle_zoom(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 and config.ZOOM < 1.6:  # колесико вверх
                config.ZOOM *= 1.1
            elif event.button == 5 and config.ZOOM > 0.55:  # колесико вниз
                config.ZOOM /= 1.1

    def handle_event(self, event):
        if event.type == events.GAME_OVER:
            self.stop()

        elif event.type == events.OBJECT_DESTRUCTION:
            if event.object in self.space_objects:
                self.physical_space.remove(event.object)
                self.space_objects.remove(event.object)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.trigger_event(events.OPEN_PAUSE_MENU)

    def update(self):
        self.physical_space.get_simulation_step()
        self.camera.update(self.player_ship)

        self.player_ship.update_rotate_point(self.camera)

        self.background.move(self.player_ship.body.velocity)
        self.planets.move(self.player_ship.body.velocity)

    def draw(self):
        keys = pygame.key.get_pressed()

        self.player_ship.inactivity_animation()

        # движение по нажатию на кнопку W
        if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
            self.player_ship.accelerator_animation()
            self.player_ship.move_ship()
            self.player_ship.draw(self.screen, self.camera)

            # ускорение
            if keys[pygame.K_LALT]:
                pass

        elif keys[pygame.K_SPACE]:
            self.player_ship.deceleration_ship()

        # Рисуем корабль
        self.player_ship.rotate_animation()
        self.player_ship.draw(self.screen, self.camera)

        for obj in self.space_objects:
            obj.draw(self.screen, self.camera)

        # Отрисовка объектов Pymunk
        self.physical_space.space.debug_draw(self.draw_options)
