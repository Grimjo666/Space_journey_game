import pygame

import config
from engine import events


class BaseScene:
    def __init__(self, screen):
        self.active = True
        self.screen = screen

    @staticmethod
    def trigger_event(event):
        repeat_event = pygame.event.Event(event)
        pygame.event.post(repeat_event)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def start(self):
        self.active = True

    def scene(self):
        if self.active:
            self.update()
            self.draw()

    def stop(self):
        self.active = False

    def create_objects(self):
        pass


class SceneManager:
    def __init__(self, scenes=None):
        """
        :param scenes: dict. Сцены, имеют приоритет по расположению,
         последняя сцена в словаре будет рисоваться поверх остальных
        """
        if scenes:
            if isinstance(scenes, dict):
                self.scenes = scenes
            else:
                raise ValueError(f'Аргумент scenes должен быть dict, а передаётся {type(scenes)}')

        self.scenes = {}
        self.current_scene = None
        self.running = True

    def add_scene(self, name, scene, active=True):
        """
        При добавлении новой сцены, она получает приоритет при рендеринге (если она активна)
        :param name:
        :param scene:
        :param active: Если передать False, то сцены будут добавляться выключенными
        :return:
        """
        if isinstance(scene, BaseScene):
            self.scenes[name] = scene

            if not active:
                self.scenes[name].stop()
        else:
            raise ValueError(f'Аргумент scene не является сценой, а передаётся {type(scene)}')

    def get_scene(self, name):
        return self.scenes[name]

    def stop_all(self):
        for scene in self.scenes.values():
            scene.stop()

    def handle_events(self, event):
        for scene in self.scenes.values():
            if scene.active:
                scene.handle_event(event)

    def draw_scenes(self):
        for scene in self.scenes.values():
            scene.scene()
