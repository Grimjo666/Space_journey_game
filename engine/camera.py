import pygame
import pymunk

import config


class Camera:
    def __init__(self):
        self.camera = pygame.Rect(0, 0, config.WORLD_WIDTH, config.WORLD_HEIGHT)
        self.width = config.WORLD_WIDTH
        self.height = config.WORLD_HEIGHT

    def apply(self, position):
        return position[0] - self.camera.x, position[1] - self.camera.y

    def update(self, target):
        # Центрировать камеру на игроке
        x = -target.body.position.x + config.WIDTH / 2
        y = -target.body.position.y + config.HEIGHT / 2

        # Ограничение позиции камеры, чтобы она не выходила за границы игрового мира
        x = min(0, x)  # Не двигаться дальше левой границы
        y = min(0, y)  # Не двигаться дальше верхней границы
        x = max(-(self.width - config.WIDTH), x)  # Не двигаться дальше правой границы
        y = max(-(self.height - config.HEIGHT), y)  # Не двигаться дальше нижней границы

        self.camera = pygame.Rect(-x, -y, self.width, self.height)
