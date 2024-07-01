import math

import pygame
import random

import pymunk

import config
from engine.ships import Cruiser


class BasicPatrolling:
    # def __init__(self):
    #     self.patrol_area = 700, 700
    #     self.patrol_points = [pymunk.Vec2d(500, 300), pymunk.Vec2d(630, 1000)]
    #     self.current_point_index = 0
    #
    #     self.ship = Cruiser((0, 0))
    #
    # def patrol(self):
    #     target_pos = self.patrol_points[self.current_point_index]
    #     print(self.ship.body.position.length)
    #     self.ship.rotate_animation(target_pos)
    #
    #     if self.ship.body.position.length < target_pos.length:
    #         self.ship.move_ship()
    #     else:
    #         self.ship.deceleration_ship()
    #         self.current_point_index += 1
    #         if self.current_point_index == len(self.patrol_points):
    #             self.current_point_index = 0

    def __init__(self, ship):
        self.ship = ship
        self.start_point = self.ship.body.position

        self.patrol_points = None
        self.update_patrol_points()

        self.current_point_index = 0
        self.state = 'patrolling'
        self.move = True
        self.move_delay = 15

    def update_patrol_points(self):
        self.patrol_points = [
            (random.randint(1, 1500), random.randint(1, 1500)) for i in range(random.randrange(3, 10))
        ]

    def update_patrol(self):
        target_point = self.patrol_points[self.current_point_index]

        if self.current_point_index == len(self.patrol_points):
            self.update_patrol_points()

        target_angle = self.ship.calculate_angle(target_point)
        current_angle = self.ship.body.angle
        angle_difference = abs(target_angle - current_angle)

        if not angle_difference < math.radians(1):  # Если корабль смотрит в направлении цели

            # Повернуть корабль в направлении следующей точки патруля
            self.ship.rotate_animation(target_angle)
            print('rotate')

        else:
            self.ship.body.angle = target_angle
            distance_to_target = self.ship.body.position.get_distance(target_point)
            current_speed = self.ship.body.velocity.length

            # Если расстояние до цели больше текущей скорости, двигаться
            if distance_to_target > current_speed and self.move:
                self.ship.move_ship()
                self.ship.update_rotate_point()
                print('move')
            else:
                # Тормозить, если расстояние до цели меньше порога
                self.ship.deceleration_ship()
                self.move = False
                print('break')
                # Если корабль почти остановился, перейти к следующей точке
                if current_speed < 1:  # Можно задать пороговое значение для остановки
                    self.move = True
                    self.current_point_index = (self.current_point_index + 1) % len(self.patrol_points)

    def update(self):
        if self.state == 'patrolling':
            self.update_patrol()

        # Обновить положение и повернуть спрайт
        self.ship.rotate_sprite()
