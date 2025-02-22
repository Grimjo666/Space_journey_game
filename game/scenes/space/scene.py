import pygame
import pymunk
import pymunk.pygame_util
import random

from engine import events, scene
from engine.camera import Camera
from engine.scene import Grid
from engine.space import PhysicalSpace

from game.scenes.space.npcs.space_ships import ShipsNPCManager
from game.scenes.space.space_body_templates import Meteorite, Meteorite2
from game.scenes.space.background import SpaceBG, SpaceBGPlanets
from game.scenes.space.ship_templates import Cruiser
from game import config


WORLD_SCALE = 10000, 10000


class Player(Cruiser):
    OBJECT_TYPE = 'player'


class SpaceScene(scene.BaseScene):
    def __init__(self, screen):
        super().__init__(screen)

        self.camera = Camera()

        self.background = SpaceBG(screen)
        self.planets = SpaceBGPlanets(self.background.surface)
        self.physical_space = PhysicalSpace()
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)

        # звуки
        self.bg_sound = pygame.mixer.Sound('game/sounds/bg_sound.mp3')
        self.bg_sound.set_volume(config.BG_SOUND)
        self.bg_sound.play()

        self.screen_center = config.WIDTH // 2, config.HEIGHT // 2

        self.player_ship = Player(self.screen_center)
        self.npc_manager = None

        self.grid = Grid(world_scale=WORLD_SCALE, cell_size=500)  # Сетка с игровыми объектами

    def create_objects(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        for obj in [
            Meteorite((100, 900)),
            Meteorite((300, 1000)),
            Meteorite((config.WIDTH, config.HEIGHT)),
            Meteorite2((500, 500)),
            Meteorite2((900, 900)),
            *[Meteorite((random.randrange(-10000, 10000), random.randrange(-10000, 10000))) for _ in range(100)],
            *[Meteorite2((random.randrange(-10000, 10000), random.randrange(-10000, 10000))) for _ in range(100)]
        ]:
            self.grid.add_object(obj)

        self.grid.add_object(self.player_ship)

        self.npc_manager = ShipsNPCManager()

        for npc in self.npc_manager.get_npc():
            self.grid.add_object(npc.ship)

        for obj in self.grid.get_all_obj():
            self.physical_space.add(obj)

    def handle_event(self, event):
        if event.type == events.GAME_OVER:
            self.stop()

        elif event.type == events.OBJECT_DESTRUCTION:
            if event.object in self.grid.get_all_obj():
                self.physical_space.remove(event.object)

                self.grid.remove(event.object)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.trigger_event(events.OPEN_PAUSE_MENU)

    def update(self):

        if not self.time_running:
            self.start_time = pygame.time.get_ticks()
            self.time_running = True

        # Обновляем время внутри сцены
        self.time = (pygame.time.get_ticks() - self.start_time)

        self.physical_space.get_simulation_step()
        self.camera.update(self.player_ship)

        # Обновляем игрока
        self.player_ship.update(self.camera)

        # Обновляем поведение неписей
        self.npc_manager.update()

        self.background.draw(self.camera)
        self.planets.draw(self.camera)

        self.player_ship.ship_control(keys=pygame.key.get_pressed(), mouse_keys=pygame.mouse.get_pressed())

        # достаём патрон у пушки
        bullet = self.player_ship.first_weapon.get_bullet()

        # Если патрон есть, добавляем его в игровое пространство
        if bullet:
            self.grid.add_object(bullet)
            self.physical_space.add(bullet)

        # Обновляем информацию об объектах в игровой сетке
        if self.time % 200 < 50:  # обновляем сетку примерно 5 раз в секунду
            self.grid.update()

    def draw(self):

        self.npc_manager.draw(self.screen, self.camera)  # Рисуем неписей

        for obj in self.grid.get_all_obj():
            obj.draw(self.screen, self.camera)
        # Рисуем патроны
        for bullet in self.player_ship.first_weapon.bullet_list:
            bullet.draw(self.screen, self.camera)

        self.player_ship.draw(self.screen, self.camera)  # Рисуем корабль
        # Отрисовка объектов Pymunk
        self.physical_space.space.debug_draw(self.draw_options)

