import pygame

from engine.space import BaseShip
from engine.shooting import BaseBullet


class Cruiser(BaseShip):
    MAX_SPEED = 500
    MASS = 500
    ENGINE_POWER = 15
    ELASTICITY = 0.3
    FRICTION = 0.5
    SPRITE_PATH = 'game/images/space/ship_sprites/ship_2/ship_2.png'
    BASE_BULLET = BaseBullet

    HEALTH = 300

    ROTATE_SPEED = 4
    ROTATE_SLOWDOWN_THRESHOLD = 30
    MIN_ROTATE_SPEED = 2

    def __init__(self, ship_position, body_type='circle'):
        super().__init__(ship_position, body_type)
        self.radius *= 0.6

        self._accelerator_sprites = [
            pygame.image.load(f'game/images/space/ship_sprites/ship_2/accelerators/main_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self._rotate_left_sprites = [
            pygame.image.load(f'game/images/space/ship_sprites/ship_2/accelerators/rotate_left_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self._rotate_right_sprites = [
            pygame.image.load(f'game/images/space/ship_sprites/ship_2/accelerators/rotate_right_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]