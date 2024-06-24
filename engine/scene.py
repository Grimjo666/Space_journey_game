import pygame

import config
from engine import events


class BaseScene:
    def __init__(self, screen, clock):
        self.active = True
        self.screen = screen
        self.clock = clock

    @staticmethod
    def event_repeater(event):
        repeat_event = pygame.event.Event(event)
        pygame.event.post(repeat_event)

    def event_dispatch_above(self, event):
        self.stop()
        self.event_repeater(event)

    def _handle_events(self):
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.event_dispatch_above(pygame.QUIT)

            self.handle_event(event)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def start(self):
        self.active = True

    def scene(self):
        while self.active:
            self._handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def stop(self):
        self.active = False
