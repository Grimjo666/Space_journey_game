import math
import pygame
import pymunk

import config
from .space import SpaceObject


class BaseShip(SpaceObject):
    MAX_SPEED = 0
    ENGINE_POWER = 0

    ROTATE_SPEED = 0
    ROTATE_SLOWDOWN_THRESHOLD = 0
    MIN_ROTATE_SPEED = 0

    def __init__(self, ship_position,  body_type='circle'):
        super().__init__(ship_position, body_type)

        self._accelerator_sprites = None
        self._rotate_left_sprites = None
        self._rotate_right_sprites = None
        self.motion_sprite_counter = -1
        self.rotate_point = self.body.position

        self.move_vector = pymunk.Vec2d(0, 0)

    def update_rotate_point(self, camera=None):
        if camera:
            self.rotate_point = camera.apply(self.body.position)
        else:
            self.rotate_point = self.body.position

    def calculate_angle(self, target_pos=None):
        if target_pos:
            m_x, m_y = target_pos
        else:
            m_x, m_y = pygame.mouse.get_pos()

        p_x, p_y = self.rotate_point

        result_angle = math.atan2(m_y - p_y, m_x - p_x)

        if result_angle < 0:  # Если угол отрицательный, добавляем 2 * пи
            result_angle += 2 * math.pi

        return result_angle

    def get_movement_vector(self):

        # Вычисление изменений по осям x и y
        dx = self.MAX_SPEED * math.cos(self.body.angle)
        dy = self.MAX_SPEED * math.sin(self.body.angle)

        self.move_vector = pymunk.Vec2d(dx, dy)

    def smooth_rotation(self, target_angle=None):
        # Логика поворота с симуляцией массы корабля
        if not target_angle:
            target_angle = self.calculate_angle()

        current_angle = self.body.angle
        difference = target_angle - current_angle

        if abs(difference) <= 0.01:
            difference = 0

        if difference > math.pi:
            difference -= 2 * math.pi
        elif difference < -math.pi:
            difference += 2 * math.pi

        # Замедление в конце поворота
        if abs(difference) < self.ROTATE_SLOWDOWN_THRESHOLD:
            rotate_speed = max(self.MIN_ROTATE_SPEED,
                               self.ROTATE_SPEED * abs(difference) // self.ROTATE_SLOWDOWN_THRESHOLD)
        else:
            rotate_speed = self.ROTATE_SPEED

        # Применение угловой скорости
        if difference != 0:
            target_angular_velocity = math.copysign(rotate_speed, difference)

            # Ограничиваем угловую скорость
            max_angular_velocity = rotate_speed
            self.body.angular_velocity = max(min(target_angular_velocity, max_angular_velocity), -max_angular_velocity)

        else:
            self.body.angular_velocity = 0

        # Применяем угловую скорость к текущему углу
        self.body.angle += self.body.angular_velocity

        # Убедитесь, что угол остается в диапазоне от 0 до 2*pi
        self.body.angle %= 2 * math.pi
        if self.body.angle < 0:
            self.body.angle += 2 * math.pi

    def move_ship(self):
        self.accelerator_animation()
        self.get_movement_vector()

        impulse = self.move_vector * self.ENGINE_POWER
        self.body.apply_impulse_at_world_point(impulse, (0, 0))
        self.limit_velocity()

    def deceleration_ship(self):
        if self.body.velocity.length < self.MAX_SPEED * 0.1:
            self.body.velocity = pymunk.Vec2d(0, 0)
        else:
            self.body.velocity *= 0.95

    def limit_velocity(self):
        if self.body.velocity.length > self.MAX_SPEED:
            self.body.velocity = self.body.velocity.normalized() * self.MAX_SPEED

    def rotate_sprite(self):
        return pygame.transform.rotate(self.current_sprite, -math.degrees(self.body.angle) - 90)

    def accelerator_animation(self):
        self.motion_sprite_counter += 1
        if self.motion_sprite_counter == 4:
            self.motion_sprite_counter = 0

        self.current_sprite = self._accelerator_sprites[self.motion_sprite_counter]

    def rotate_animation(self, target_angle=None):
        # Активируем вращение корабля
        self.smooth_rotation(target_angle)

        if not target_angle:
            target_angle = self.calculate_angle()

        difference = target_angle - self.body.angle
        if difference > math.pi:
            difference -= 2 * math.pi
        elif difference < -math.pi:
            difference += 2 * math.pi

        # Если разница в углах больше, то вычисляем направление вращения
        if abs(difference) > math.radians(0.5):
            if difference < 0:
                self.motion_sprite_counter = (self.motion_sprite_counter + 1) % len(self._rotate_left_sprites)
                self.current_sprite = self._rotate_left_sprites[self.motion_sprite_counter]
            else:
                self.motion_sprite_counter = (self.motion_sprite_counter + 1) % len(self._rotate_right_sprites)
                self.current_sprite = self._rotate_right_sprites[self.motion_sprite_counter]
        else:
            self.current_sprite = self._sprite

    def inactivity_animation(self):
        self.current_sprite = self._sprite


class Cruiser(BaseShip):
    MAX_SPEED = 500
    MASS = 500
    ENGINE_POWER = 15
    ELASTICITY = 0.3
    FRICTION = 0.5
    SPRITE_PATH = 'images/space/ship_sprites/ship_2/ship_2.png'

    HEALTH = 300

    ROTATE_SPEED = math.radians(3)
    ROTATE_SLOWDOWN_THRESHOLD = math.radians(30)
    MIN_ROTATE_SPEED = math.radians(1)

    def __init__(self, ship_position, body_type='circle'):
        super().__init__(ship_position, body_type)
        self.radius *= 0.6

        self._accelerator_sprites = [
            pygame.image.load(f'images/space/ship_sprites/ship_2/accelerators/main_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self._rotate_left_sprites = [
            pygame.image.load(f'images/space/ship_sprites/ship_2/accelerators/rotate_left_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self._rotate_right_sprites = [
            pygame.image.load(f'images/space/ship_sprites/ship_2/accelerators/rotate_right_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
