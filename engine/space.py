import math

import pygame
import pymunk

import config


class Utils:
    @staticmethod
    def lerp(start, end, proportion):
        return round(start + (end - start) * proportion, 3)

    @staticmethod
    def invert_two_digit(digit):
        return -digit[0], -digit[1]


# class ScaledSurface:
#     def __init__(self, width, height):
#         self.width = width * 2
#         self.height = height * 2
#         self.temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
#         self.center = (width, height)
#
#     def add(self, space_obj):
#         from .ships import BaseShip
#
#         sprite = space_obj.sprite
#         if isinstance(space_obj, BaseShip):
#             sprite = space_obj.current_sprite
#
#         correct_position = (
#             self.center[0] + (space_obj.body.position.x - self.center[0]),
#             self.center[1] + (space_obj.body.position.y - self.center[1])
#         )
#
#         rect = sprite.get_rect(center=correct_position)
#         self.temp_surface.blit(sprite, rect.topleft)
#
#     def draw_on_screen(self, screen):
#         scaled_surface = pygame.transform.scale(
#             self.temp_surface,
#             (int(self.width * config.ZOOM), int(self.height * config.ZOOM))
#         )
#
#         scaled_rect = scaled_surface.get_rect(center=screen.get_rect().center)
#         screen.blit(scaled_surface, scaled_rect)


class PhysicalSpace:
    def __init__(self):
        self.space = pymunk.Space()
        self.handler = self.space.add_collision_handler(1, 1)
        self.handler.begin = self.damage_handler

    def add(self, obj):
        self.space.add(obj.body, obj.get_shape())

    def remove(self, objs):
        self.space.remove(objs)

    def move_camera(self, camera_offset):
        for body in self.space.bodies:
            body.position += camera_offset

    def get_simulation_step(self):
        return self.space.step(1 / config.FPS)

    def damage_handler(self, arbiter, space, data):
        for shape in arbiter.shapes:
            print(str(shape.object_data))
            print(shape.object_data.body.velocity.length)
        return True


class SpaceBG:
    def __init__(self, surface):
        self.surface = surface
        self.bg_color = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.bg_color.fill((33, 9, 74))
        self.stars_bg_x = self.stars_bg_y = 0
        self.stars_bg = pygame.image.load('images/space/stars.png').convert_alpha()

    def move_camera(self, camera_offset):
        x, y = camera_offset
        self.update_coordinates(-x, y)

        self.surface.blit(self.bg_color, (0, 0))

        self.surface.blit(self.stars_bg, (self.stars_bg_x, self.stars_bg_y))
        self.surface.blit(self.stars_bg, (self.stars_bg_x, self.stars_bg_y - config.HEIGHT))
        self.surface.blit(self.stars_bg, (self.stars_bg_x, self.stars_bg_y + config.HEIGHT))
        self.surface.blit(self.stars_bg, (self.stars_bg_x - config.WIDTH, self.stars_bg_y))
        self.surface.blit(self.stars_bg, (self.stars_bg_x + config.WIDTH, self.stars_bg_y))
        self.surface.blit(self.stars_bg, (self.stars_bg_x - config.WIDTH, self.stars_bg_y - config.HEIGHT))
        self.surface.blit(self.stars_bg, (self.stars_bg_x + config.WIDTH, self.stars_bg_y + config.HEIGHT))
        self.surface.blit(self.stars_bg, (self.stars_bg_x - config.WIDTH, self.stars_bg_y + config.HEIGHT))
        self.surface.blit(self.stars_bg, (self.stars_bg_x + config.WIDTH, self.stars_bg_y - config.HEIGHT))

    def update_coordinates(self, speed_x, speed_y):
        stars_bg_x = self.stars_bg_x - speed_x * 0.1
        stars_bg_y = self.stars_bg_y + speed_y * 0.1

        # Зацикливание спрайта звёзд
        if -config.WIDTH >= self.stars_bg_x or self.stars_bg_x >= config.WIDTH:
            stars_bg_x = 0
        if -config.HEIGHT >= self.stars_bg_y or self.stars_bg_y >= config.HEIGHT:
            stars_bg_y = 0

        self.stars_bg_x = stars_bg_x
        self.stars_bg_y = stars_bg_y


class SpaceObject:
    """
    collision_type = 1 - Космический мусор
    """
    MAX_SPEED = 0
    MASS = 1
    ELASTICITY = 0
    FRICTION = 0

    HEALTH = 1

    SPRITE_PATH = None

    def __init__(self, position, body_type='circle'):
        self.health = self.HEALTH

        self.sprite = pygame.image.load(self.SPRITE_PATH).convert_alpha()
        self._current_sprite = self.sprite

        self.original_radius = self.sprite.get_rect().width // 2
        self.radius = self.original_radius

        self.original_mass = self.MASS
        self.mass = self.MASS

        if body_type == 'circle':
            self.body = pymunk.Body(self.mass, pymunk.moment_for_circle(self.mass, 0, self.radius))
            self.body.type = 'circle'
        elif body_type == 'box':
            self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, self.sprite.get_size()))
            self.body.type = 'box'
        self.body.position = position

    def change_scale(self):
        # Обновляем положение тела
        self.body.position = pymunk.Vec2d(self.body.position.x * config.ZOOM, self.body.position.y * config.ZOOM)

        # Обновляем радиус и массу
        self.radius = self.original_radius * config.ZOOM
        self.mass = self.original_mass * config.ZOOM

        # Обновляем момент инерции тела
        self.body.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)

        # Обновляем спрайт
        rect = self.sprite.get_rect()
        self.current_sprite = pygame.transform.scale(self.sprite,
                                                     (int(rect.width * config.ZOOM), int(rect.height * config.ZOOM)))

    def get_circle_shape(self):
        circle_shape = pymunk.Circle(self.body, self.radius)
        circle_shape.elasticity = self.ELASTICITY
        circle_shape.friction = self.FRICTION
        circle_shape.collision_type = 1
        circle_shape.object_data = self
        return circle_shape

    def get_box_shape(self):
        box_shape = pymunk.Poly.create_box(self.body, self.sprite.get_size())
        box_shape.elasticity = self.ELASTICITY
        box_shape.collision_type = 1
        box_shape.object_data = self
        return box_shape

    def get_shape(self):
        if self.body.type == 'circle':
            return self.get_circle_shape()
        elif self.body.type == 'box':
            return self.get_box_shape()

    def draw(self, surface, sprite=None):
        if sprite is None:
            sprite = self._current_sprite

        rect = sprite.get_rect(center=self.body.position)
        surface.blit(sprite, rect.topleft)

    def rotate_sprite(self):
        self._current_sprite = pygame.transform.rotate(self._current_sprite, -math.degrees(self.body.angle) - 90)

    @property
    def current_sprite(self):
        self.rotate_sprite()
        return self._current_sprite

    @current_sprite.setter
    def current_sprite(self, value):
        self._current_sprite = value


class Meteorite(SpaceObject):
    MASS = 1000
    ELASTICITY = 0.5
    FRICTION = 1
    SPRITE_PATH = 'images/space_objects/meteorites/meteorite_1.png'

    HEALTH = 100
