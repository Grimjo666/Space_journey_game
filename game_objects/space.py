import pygame

import config


class SpaceBG:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.bg_color.fill((33, 9, 74))
        self.stars_bg_x = self.stars_bg_y = 0
        self.stars_bg = pygame.image.load('images/space/stars.png').convert_alpha()

    def draw_stars_bg(self, speed_x, speed_y):
        self.update_coordinates(speed_x, speed_y)

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
