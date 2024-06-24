import pygame
import pygame.gfxdraw

import config
from engine import events, scene
from engine.menu import MainMenu
from scenes.space import SpaceScene


class MainMenuScene(scene.BaseScene):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)

        self.background = pygame.image.load('images/main_menu/background/galaxy-space.jpg').convert()

        self.menu = MainMenu()

        self.space_scene = SpaceScene(screen, clock)

        self.menu.margin_left = 20
        self.menu.margin_top = 10

        self.transparent_box = pygame.Surface((500, 400), pygame.SRCALPHA)
        self.transparent_box.fill((0, 0, 0, 128))
        box_pos = self.screen.get_rect().bottomleft
        box_pos = box_pos[0] + 20, box_pos[1] - 20
        self.transparent_box_rect = self.transparent_box.get_rect(bottomleft=box_pos)

    def handle_event(self, event):
        if event.type == events.NEW_GAME:
            self.event_dispatch_above(events.NEW_GAME)

    def draw(self):
        self.menu.draw(self.transparent_box, self.transparent_box_rect)

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.transparent_box, self.transparent_box_rect)

