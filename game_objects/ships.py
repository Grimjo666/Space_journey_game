import math
import pygame
import pymunk

from .space import SpaceObject


class BaseShip(SpaceObject):
    MAX_SPEED = 0
    ENGINE_POWER = 0

    ROTATE_SPEED = 0
    ROTATE_SLOWDOWN_THRESHOLD = 0
    MIN_ROTATE_SPEED = 0

    def __init__(self, ship_position):
        super().__init__(ship_position)
        self.current_sprite = None

        self.accelerator_sprites = None
        self.rotate_left_sprites = None
        self.rotate_right_sprites = None
        self.motion_sprite_counter = -1

        self.move_vector = pymunk.Vec2d(0, 0)
        self.current_angle = 0

    def calculate_angle(self):
        m_x, m_y = pygame.mouse.get_pos()
        p_x, p_y = self.body.position

        result_angle = math.atan2(p_y - m_y, m_x - p_x)

        if result_angle < 0:  # Если угол отрицательный, добавляем 2 * пи
            result_angle += 2 * math.pi

        return int(result_angle * 180 / math.pi)

    def get_movement_vector(self):
        # Преобразование угла из градусов в радианы
        radian_angle = math.radians(self.current_angle)

        # Вычисление изменений по осям x и y
        dx = round(self.MAX_SPEED * math.cos(radian_angle), 3)
        dy = round(self.MAX_SPEED * math.sin(radian_angle), 3)

        self.move_vector = pymunk.Vec2d(dx, -dy)

    def smooth_rotation(self):
        # Логика поворота с симуляцией массы корабля
        difference = self.calculate_angle() - self.current_angle
        if difference > 180:
            difference -= 360
        elif difference < -180:
            difference += 360

        # Замедление в конце поворота
        if abs(difference) < self.ROTATE_SLOWDOWN_THRESHOLD:
            rotate_speed = max(self.MIN_ROTATE_SPEED,
                               self.ROTATE_SPEED * abs(difference) // self.ROTATE_SLOWDOWN_THRESHOLD)
        else:
            rotate_speed = self.ROTATE_SPEED

        if difference != 0:

            if abs(difference) < rotate_speed:
                self.current_angle += difference
            else:
                self.current_angle += math.copysign(rotate_speed, difference)

        self.current_angle %= 360

    @staticmethod
    def lerp(start, end, proportion):
        return round(start + (end - start) * proportion, 3)

    def move_ship(self):
        self.get_movement_vector()

        impulse = self.move_vector * self.ENGINE_POWER
        self.body.apply_impulse_at_local_point(impulse)
        self.limit_velocity()

    def deceleration_ship(self):
        if self.body.velocity.length < self.MAX_SPEED * 0.1:
            self.body.velocity = pymunk.Vec2d(0, 0)
        else:
            self.body.velocity *= 0.95

    def limit_velocity(self):
        if self.body.velocity.length > self.MAX_SPEED:
            self.body.velocity = self.body.velocity.normalized() * self.MAX_SPEED

    def draw_ship(self, surface, sprite):
        if sprite is None:
            sprite = self.sprite

        sprite = pygame.transform.rotate(sprite, self.current_angle - 90)
        player_rect = sprite.get_rect(center=self.body.position)
        surface.blit(sprite, player_rect.topleft)

    def accelerator_animation(self, surface):
        self.motion_sprite_counter += 1
        if self.motion_sprite_counter == 4:
            self.motion_sprite_counter = 0

        sprite = self.current_sprite = self.accelerator_sprites[self.motion_sprite_counter]
        self.draw_ship(surface, sprite)

    def rotate_animation(self, surface):
        # Активируем вращение корабля
        self.smooth_rotation()

        difference = self.calculate_angle() - self.current_angle
        if difference > 180:
            difference -= 360
        elif difference < -180:
            difference += 360

        # Если разница в углах больше, то вычисляем направление вращения
        if abs(difference) > 0.5:
            if difference > 0:
                self.motion_sprite_counter = (self.motion_sprite_counter + 1) % len(self.rotate_left_sprites)
                self.current_sprite = self.rotate_left_sprites[self.motion_sprite_counter]
            else:
                self.motion_sprite_counter = (self.motion_sprite_counter + 1) % len(self.rotate_right_sprites)
                self.current_sprite = self.rotate_right_sprites[self.motion_sprite_counter]
        else:
            self.current_sprite = self.sprite

        self.draw_ship(surface, self.current_sprite)

    def inactivity_animation(self):
        self.current_sprite = self.sprite


class Cruiser(BaseShip):
    MAX_SPEED = 300
    MASS = 500
    ENGINE_POWER = 15
    ELASTICITY = 0.3
    SPRITE_PATH = 'images/ship_sprites/ship_2/ship_2.png'

    ROTATE_SPEED = 3
    ROTATE_SLOWDOWN_THRESHOLD = 60
    MIN_ROTATE_SPEED = 1

    def __init__(self, ship_position):
        super().__init__(ship_position)
        self.radius = self.radius * 0.6

        self.accelerator_sprites = [
            pygame.image.load(f'images/ship_sprites/ship_2/accelerators/main_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self.rotate_left_sprites = [
            pygame.image.load(f'images/ship_sprites/ship_2/accelerators/rotate_left_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self.rotate_right_sprites = [
            pygame.image.load(f'images/ship_sprites/ship_2/accelerators/rotate_right_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
