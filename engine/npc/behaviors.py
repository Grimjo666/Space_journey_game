import pygame
import random


class BasePatrolling:

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
            (random.randint(1, 3500), random.randint(1, 3500)) for i in range(random.randrange(3, 10))
        ]

    def update(self):
        target_point = self.patrol_points[self.current_point_index]
        self.ship.update()
        keys_dict = {
            pygame.K_w: False,
            pygame.K_SPACE: False,
            pygame.K_LALT: False
        }

        target_angle = self.ship.calculate_angle(target_point)
        current_angle = self.ship.body.angle
        angle_difference = abs(target_angle - current_angle)

        if angle_difference < 0.08:
            self.ship.body.angle = target_angle
            distance_to_target = self.ship.body.position.get_distance(target_point)
            current_speed = self.ship.body.velocity.length

            # Если расстояние до цели больше текущей скорости, двигаться
            if distance_to_target > current_speed and self.move:
                keys_dict[pygame.K_w] = True

            else:
                # Тормозить, если расстояние до цели меньше порога
                keys_dict[pygame.K_SPACE] = True
                self.move = False

                # Если корабль почти остановился, перейти к следующей точке
                if current_speed < 1:  # Можно задать пороговое значение для остановки
                    self.move = True

                    # Проверяем пройдена ли последняя патрульная точка
                    if self.current_point_index == len(self.patrol_points) - 1:
                        # Обновляем список с точками
                        self.update_patrol_points()

                    self.current_point_index = (self.current_point_index + 1) % len(self.patrol_points)

        self.ship.ship_control(keys=keys_dict, mouse_keys=[False, False, False], target_angle=target_angle)

    def draw_patrole_points(self, screen, camera):
        """
        Отладочный метод
        :param screen:
        :param camera:
        :return:
        """
        for position in self.patrol_points:
            position = camera.apply(position)
            rect = pygame.Rect(*position, 40, 40)
            pygame.draw.rect(screen, 'red', rect)
