import pygame
import pymunk

import config


class SpaceBG:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.bg_color.fill((33, 9, 74))
        self.stars_bg_x = self.stars_bg_y = 0
        self.stars_bg = pygame.image.load('images/space/stars.png').convert_alpha()

    def draw_stars_bg(self, speed_x, speed_y):
        self.update_coordinates(-speed_x, speed_y)

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
        stars_bg_x = self.stars_bg_x - speed_x / 10
        stars_bg_y = self.stars_bg_y + speed_y / 10

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

        self.radius = self.sprite.get_rect().width // 2

        self.body = pymunk.Body(self.MASS, pymunk.moment_for_circle(self.MASS, 0, self.radius))
        self.body.position = position
        self.speed_x = self.speed_y = 0

    def get_circle_shape(self):
        circle_shape = pymunk.Circle(self.body, self.radius)
        circle_shape.elasticity = self.ELASTICITY
        return circle_shape

    def draw(self, surface, sprite=None):
        if sprite is None:
            sprite = self.sprite

        rect = self.sprite.get_rect(center=self.body.position)
        surface.blit(sprite, rect.topleft)


class Meteorite(SpaceObject):
    MASS = 100
    ELASTICITY = 0.5
    SPRITE_PATH = 'images/space_objects/meteorites/meteorite_1.png'
