import pygame
import pymunk

import engine.space


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera_offset = 0, 0
        self.view_rect = pygame.Rect(0, 0, width, height)
        self.previous_frames = []
        self.max_frames = 7  # Количество предыдущих кадров для размытия

    def update(self, player_pos):
        player_x, player_y = player_pos
        self.camera_offset = pymunk.Vec2d(self.width // 2 - player_x,
                                          self.height // 2 - player_y)

    def apply(self, obj):
        obj.move(self.camera_offset)

    def clear_frames(self):
        self.previous_frames.clear()

    def draw_blur(self, surface):
        if len(self.previous_frames) == self.max_frames:
            self.previous_frames.pop(0)

        self.previous_frames.append(surface.copy())

        for i, frame in enumerate(reversed(self.previous_frames)):
            alpha = int(255 / (i + 2))
            frame.set_alpha(alpha)
            surface.blit(frame, (0, 0))

    def is_visible(self, obj):
        if isinstance(obj, pymunk.Body):
            return self.view_rect.collidepoint(obj.position)
        else:
            return self.view_rect.colliderect(obj.rect)