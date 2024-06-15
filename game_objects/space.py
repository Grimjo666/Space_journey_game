import pygame
import pymunk

import config


class PhysicalSpace:
    def __init__(self):
        self.space = pymunk.Space()

    def add(self, obj):
        self.space.add(obj.body, obj.get_circle_shape())

    def remove(self, objs):
        self.space.remove(objs)

    def move_camera(self, camera_offset):
        for body in self.space.bodies:
            body.position += camera_offset

    def get_simulation_step(self):
        return self.space.step(1 / config.FPS)


class SpaceBG:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.bg_color.fill((33, 9, 74))
        self.stars_bg_x = self.stars_bg_y = 0
        self.stars_bg = pygame.image.load('images/space/stars.png').convert_alpha()

    def move_camera(self, camera_offset):
        x, y = camera_offset * config.ZOOM
        self.update_coordinates(-x, y)

        self.screen.blit(self.bg_color, (0, 0))

        self.screen.blit(self.stars_bg, (self.stars_bg_x, self.stars_bg_y))
        self.screen.blit(self.stars_bg, (self.stars_bg_x, self.stars_bg_y - config.HEIGHT))
        self.screen.blit(self.stars_bg, (self.stars_bg_x, self.stars_bg_y + config.HEIGHT))
        self.screen.blit(self.stars_bg, (self.stars_bg_x - config.WIDTH, self.stars_bg_y))
        self.screen.blit(self.stars_bg, (self.stars_bg_x + config.WIDTH, self.stars_bg_y))
        self.screen.blit(self.stars_bg, (self.stars_bg_x - config.WIDTH, self.stars_bg_y - config.HEIGHT))
        self.screen.blit(self.stars_bg, (self.stars_bg_x + config.WIDTH, self.stars_bg_y + config.HEIGHT))
        self.screen.blit(self.stars_bg, (self.stars_bg_x - config.WIDTH, self.stars_bg_y + config.HEIGHT))
        self.screen.blit(self.stars_bg, (self.stars_bg_x + config.WIDTH, self.stars_bg_y - config.HEIGHT))

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
    MAX_SPEED = 0
    MASS = 1
    ELASTICITY = 0

    SPRITE_PATH = None

    def __init__(self, position):
        self.sprite = pygame.image.load(self.SPRITE_PATH).convert_alpha()

        self.radius = (self.sprite.get_rect().width * config.ZOOM) // 2

        self.body = pymunk.Body(self.MASS, pymunk.moment_for_circle(self.MASS, 0, self.radius))
        self.body.position = position

    def get_circle_shape(self):
        circle_shape = pymunk.Circle(self.body, self.radius)
        circle_shape.elasticity = self.ELASTICITY
        return circle_shape

    def draw(self, surface, sprite=None):
        if sprite is None:
            sprite = self.sprite

        scaled_sprite = pygame.transform.scale(sprite, (
            int(sprite.get_width() * config.ZOOM),
            int(sprite.get_height() * config.ZOOM)
        ))
        rect = scaled_sprite.get_rect(center=self.body.position)
        surface.blit(scaled_sprite, rect.topleft)


class Meteorite(SpaceObject):
    MASS = 1000
    ELASTICITY = 0.5
    SPRITE_PATH = 'images/space_objects/meteorites/meteorite_1.png'
