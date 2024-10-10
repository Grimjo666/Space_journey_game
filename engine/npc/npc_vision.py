import pygame
import math

from engine.tools import coord_adjustment


NUM_RAYS = 30
VIEW_RADIUS = 300


def cast_ray(npc_pos, direction, objects, camera):
    """Запускает один луч и проверяет пересечение со спрайтами."""
    end_x = npc_pos[0] + VIEW_RADIUS * math.cos(direction)
    end_y = npc_pos[1] + VIEW_RADIUS * math.sin(direction)
    ray_end = end_x, end_y

    # Проверка пересечения луча со спрайтами
    for obj in objects:
        # print(obj.ship.current_sprite.get_rect())
        intersect_point = check_line_rect_collision(npc_pos, ray_end, obj, camera)
        if intersect_point:
            ray_end = intersect_point  # Если есть пересечение, луч заканчивается на этой точке
            break

    return ray_end


def check_line_rect_collision(p1, p2, obj, camera):
    """Проверяет пересечение линии с прямоугольником."""

    rect = obj.current_sprite.get_rect()
    obj_position = obj.body.position

    # Проверяем пересечения линии с каждой стороной прямоугольника
    rect_lines = (
        (
            camera.apply(
                coord_adjustment(obj_position, (rect.left, rect.top))
            ),
            camera.apply(
                coord_adjustment(obj_position, (rect.right, rect.top))
                         )
         ),  # Верхняя грань
        (
            camera.apply(
                coord_adjustment(obj_position, (rect.right, rect.top))
                         ),
            camera.apply(
                coord_adjustment(obj_position, (rect.right, rect.bottom))
                         )
         ),  # Правая грань
        (
            camera.apply(
                coord_adjustment(obj_position, (rect.right, rect.bottom))
            ),
            camera.apply(
                coord_adjustment(obj_position, (rect.left, rect.bottom))
                         )
        ),  # Нижняя грань
        (
            camera.apply(
                coord_adjustment(obj_position, (rect.left, rect.bottom))
                         ),
            camera.apply(
                coord_adjustment(obj_position, (rect.left, rect.top))
            )
        )  # Левая грань
    )

    for line in rect_lines:
        intersect = check_line_intersection(p1, p2, line[0], line[1])
        if intersect:
            return intersect

    return None


def check_line_intersection(p1, p2, p3, p4):
    """Проверка пересечения двух линий (p1, p2) и (p3, p4)."""

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    x_diff = (p1[0] - p2[0], p3[0] - p4[0])
    y_diff = (p1[1] - p2[1], p3[1] - p4[1])

    div = det(x_diff, y_diff)
    if div == 0:
        return None  # Линии параллельны

    d = (det(p1, p2), det(p3, p4))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div

    if min(p1[0], p2[0]) <= x <= max(p1[0], p2[0]) and min(p3[0], p4[0]) <= x <= max(p3[0], p4[0]):
        if min(p1[1], p2[1]) <= y <= max(p1[1], p2[1]) and min(p3[1], p4[1]) <= y <= max(p3[1], p4[1]):
            return x, y
    return None


def apply_rays(screen, camera, npc, objects):
    npc_cord = camera.apply(npc.body.position)

    for i in range(NUM_RAYS):
        ray_angle = (2 * math.pi / NUM_RAYS) * i
        ray_end = cast_ray(npc_cord, ray_angle, objects, camera)

        # Отрисовка луча
        pygame.draw.line(screen, 'GREEN', npc_cord, ray_end, 1)
