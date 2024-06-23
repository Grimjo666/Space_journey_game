import pygame
import pymunk
import pymunk.pygame_util

import config
from engine import ships, space, events, menu


class PauseMenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = space.SpaceBG(screen)

        # звуки
        self.bg_sound = pygame.mixer.Sound('../sounds/bg_sound.mp3')
        self.bg_sound.set_volume(config.BG_SOUND)
        self.bg_sound.play()

        self.pause_menu = menu.PauseMenu()

    def start(self):

        while self.running:
            self.pause_menu.draw(self.screen)

            # Держим цикл на правильной скорости
            self.clock.tick(config.FPS)
            # Ввод процесса (события)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == events.TO_MAIN_MENU:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            pygame.display.flip()

        pygame.quit()