import math
import pygame


class BaseShip:
    MOVE_SPEED = 0
    ROTATE_SPEED = 0
    ROTATE_SLOWDOWN_THRESHOLD = 0
    MIN_ROTATE_SPEED = 0

    def __init__(self, ship_position):
        self.ship_position = ship_position

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
        dx = round(self.MOVE_SPEED * math.cos(radian_angle), 3)
        dy = round(self.MOVE_SPEED * math.sin(radian_angle), 3)

        return dx, dy

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


class Cruiser(BaseShip):
    MOVE_SPEED = 5
    ROTATE_SPEED = 3
    ROTATE_SLOWDOWN_THRESHOLD = 60
    MIN_ROTATE_SPEED = 1
    SPRITE = pygame.image.load('images/ship_sprites/ship_2/ship_2.png')

