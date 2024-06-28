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


# class Camera:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.camera_offset = 0, 0
#         self.view_rect = pygame.Rect(0, 0, width, height)
#
#         scale = width * 0.6, height * 0.6
#         position = (width - scale[0]) / 2, (height - scale[1]) / 2
#         self.view_rect_small = pygame.Rect(position, scale)
#
#         self.previous_frames = []
#         self.max_frames = 7  # Количество предыдущих кадров для размытия
#
#     def update(self, player_pos):
#         player_x, player_y = player_pos
#         center_x, center_y = self.width // 2, self.height // 2
#
#         self.camera_offset = pymunk.Vec2d(center_x - player_x, center_y - player_y)
#
#     def apply(self, obj):
#         obj.move(self.camera_offset)
#
#     def clear_frames(self):
#         self.previous_frames.clear()
#
#     def draw_blur(self, surface):
#         if len(self.previous_frames) == self.max_frames:
#             self.previous_frames.pop(0)
#
#         self.previous_frames.append(surface.copy())
#
#         for i, frame in enumerate(reversed(self.previous_frames)):
#             alpha = int(255 / (i + 2))
#             frame.set_alpha(alpha)
#             surface.blit(frame, (0, 0))
#
#     def is_visible(self, obj):
#         if isinstance(obj, pymunk.Body):
#             return self.view_rect.collidepoint(obj.position)
#         else:
#             return self.view_rect.colliderect(obj.rect)