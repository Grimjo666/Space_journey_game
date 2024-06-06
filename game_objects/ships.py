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
        self.ship_position = ship_position
        self.speed_x = self.speed_y = 0
        self.move_vector_x = self.move_vector_y = 0


    def get_coordinates(self):
        return self.speed_x, self.speed_y

    def calculate_angle(self):
        m_x, m_y = pygame.mouse.get_pos()
        p_x, p_y = self.ship_position

        result_angle = math.atan2(p_y - m_y, m_x - p_x)

        if result_angle < 0:  # Если угол отрицательный, добавляем 2 * пи
            result_angle += 2 * math.pi

        return int(result_angle * 180 / math.pi)

    def get_movement_vector(self, angle):
        # Преобразование угла из градусов в радианы
        radian_angle = math.radians(angle)

        # Вычисление изменений по осям x и y
        dx = round(self.MAX_SPEED * math.cos(radian_angle), 3)
        dy = round(self.MAX_SPEED * math.sin(radian_angle), 3)

        self.move_vector_x = dx
        self.move_vector_y = dy

    def smooth_rotation(self, current_angle, desired_angle):
        # Логика поворота с симуляцией массы корабля
        difference = desired_angle - current_angle
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
                current_angle += difference
            else:
                current_angle += math.copysign(rotate_speed, difference)

        current_angle %= 360
        return current_angle

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

    def draw_accelerators(self):
        pass


class Cruiser(BaseShip):
    MAX_SPEED = 17
    WEIGHT = 500
    ENGINE_POWER = 20

    ROTATE_SPEED = 3
    ROTATE_SLOWDOWN_THRESHOLD = 60
    MIN_ROTATE_SPEED = 1

    def __init__(self, ship_position):
        self.sprite = pygame.image.load('images/ship_sprites/ship_2/ship_2.png').convert_alpha()
        self.accelerator_sprites = [

        ]
        super().__init__(ship_position)
