import math
import pygame


class BaseShip:
    MAX_SPEED = 0
    WEIGHT = 0
    ENGINE_POWER = 0

    ROTATE_SPEED = 0
    ROTATE_SLOWDOWN_THRESHOLD = 0
    MIN_ROTATE_SPEED = 0

    def __init__(self, ship_position):
        self.sprite = None
        self.current_sprite = None
        self.accelerator_sprites = None
        self.rotate_sprites = None
        self.motion_sprite_counter = -1

        self.ship_position = ship_position
        self.speed_x = self.speed_y = 0
        self.move_vector_x = self.move_vector_y = 0
        self.current_angle = 0

    def get_sprite(self):
        if self.current_sprite:
            sprite = self.current_sprite
        else:
            sprite = self.sprite

        return pygame.transform.rotate(sprite, self.current_angle - 90)

    def calculate_angle(self):
        m_x, m_y = pygame.mouse.get_pos()
        p_x, p_y = self.ship_position

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

        self.move_vector_x = dx
        self.move_vector_y = dy

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
        return self.current_angle

    @staticmethod
    def lerp(start, end, proportion):
        return round(start + (end - start) * proportion, 3)

    def move_ship(self):
        acceleration = self.ENGINE_POWER / self.WEIGHT
        self.speed_x = self.lerp(self.speed_x, self.move_vector_x, acceleration)
        self.speed_y = self.lerp(self.speed_y, self.move_vector_y, acceleration)

        return self.speed_x, self.speed_y

    def deceleration_ship(self):
        deceleration_x = deceleration_y = self.ENGINE_POWER / self.WEIGHT
        if abs(self.speed_x) < 2:
            deceleration_x *= 3
        if abs(self.speed_y) < 2:
            deceleration_y *= 3

        self.speed_x = self.lerp(self.speed_x, 0, deceleration_x)
        self.speed_y = self.lerp(self.speed_y, 0, deceleration_y)

        return self.speed_x, self.speed_y

    def accelerator_animation(self):
        self.motion_sprite_counter += 1
        if self.motion_sprite_counter == 4:
            self.motion_sprite_counter = 0

        self.current_sprite = self.accelerator_sprites[self.motion_sprite_counter]

    def rotate_animation(self):
        if self.current_angle < self.calculate_angle():

            self.motion_sprite_counter += 1
            if self.motion_sprite_counter == 4:
                self.motion_sprite_counter = 0

            self.current_sprite = self.rotate_sprites[self.motion_sprite_counter]
        else:
            self.current_sprite = self.sprite

    def inactivity_animation(self):
        pass


class Cruiser(BaseShip):
    MAX_SPEED = 17
    WEIGHT = 500
    ENGINE_POWER = 20

    ROTATE_SPEED = 3
    ROTATE_SLOWDOWN_THRESHOLD = 60
    MIN_ROTATE_SPEED = 1

    def __init__(self, ship_position):
        super().__init__(ship_position)
        self.sprite = pygame.image.load('images/ship_sprites/ship_2/ship_2.png').convert_alpha()
        self.accelerator_sprites = [
            pygame.image.load(f'images/ship_sprites/ship_2/accelerators/main_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
        self.rotate_sprites = [
            pygame.image.load(f'images/ship_sprites/ship_2/accelerators/rotate_left_{i}.png').convert_alpha()
            for i in range(1, 5)
        ]
