import pygame
import pymunk
import pymunk.pygame_util

import config
from engine import ships, space, events, scene
from engine.camera import Camera
from engine.npc.space_ships import SpaceShipNPCManager, NeutralShip


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
        self.npc_manager = None

        self.space_objects = None

    def create_objects(self):
        self.space_objects = [
            space.Meteorite((100, 900)),
            space.Meteorite((300, 1000)),
            space.Meteorite((config.WIDTH, config.HEIGHT)),
            space.Meteorite2((500, 500)),
            space.Meteorite2((900, 900))

        ]

        npc_tup = (
            NeutralShip((i, i))
            for i in range(1, 1001, 100)
        )

        self.npc_manager = SpaceShipNPCManager(npc_tup)

        self.physical_space.add(self.player_ship)

        for obj in self.space_objects:
            self.physical_space.add(obj)

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

        self.background.draw(self.camera)
        self.planets.draw(self.camera)

        self.player_ship.ship_control(keys=pygame.key.get_pressed())

    def draw(self):
        self.player_ship.draw(self.screen, self.camera)  # Рисуем корабль

        for obj in self.space_objects:
            obj.draw(self.screen, self.camera)

        # Отрисовка объектов Pymunk
        # self.physical_space.space.debug_draw(self.draw_options)

