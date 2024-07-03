import math

import pygame
import pymunk

import config
from engine.space import Utils


class Camera:
    def __init__(self):
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.camera = pygame.Rect(0, 0, self.width, self.height)

        self.screen_center = config.WIDTH // 2, config.HEIGHT // 2
        self.perimeter_offset = config.CAMERA_PERIMETER_OFFSET

    def apply(self, position):
        return int(position[0] - self.camera.x), int(position[1] - self.camera.y)

    def calculate_perimeter_offset(self, mouse_cord, cord, dimension):

        if mouse_cord < self.perimeter_offset:
            offset_x = config.CAMERA_MAX_OFFSET * ((self.perimeter_offset - mouse_cord) / self.perimeter_offset) ** 3
            cord -= dimension * offset_x
        elif mouse_cord > dimension - self.perimeter_offset:
            offset_x = config.CAMERA_MAX_OFFSET * ((mouse_cord - (dimension - self.perimeter_offset))
                                                   / self.perimeter_offset) ** 3
            cord += dimension * offset_x

        return cord

    def update(self, target):
        # Центрировать камеру на игроке
        x = int(target.body.position.x - self.screen_center[0])
        y = int(target.body.position.y - self.screen_center[1])

        mouse = pygame.mouse.get_pos()

        # Проверка и расчет смещения по оси X
        x = self.calculate_perimeter_offset(mouse[0], x, self.width)

        # Проверка и расчет смещения по оси Y
        y = self.calculate_perimeter_offset(mouse[1], y, self.height)

        self.camera = pygame.Rect(x, y, self.width, self.height)

        # Ограничение позиции камеры, чтобы она не выходила за границы игрового мира
        # x = min(0, x)  # Не двигаться дальше левой границы
        # y = min(0, y)  # Не двигаться дальше верхней границы
        # x = max(-(self.width - config.WIDTH), x)  # Не двигаться дальше правой границы
        # y = max(-(self.height - config.HEIGHT), y)  # Не двигаться дальше нижней границы



