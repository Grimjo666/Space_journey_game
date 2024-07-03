import math

import pygame
import pymunk

import config
from engine import events


class Utils:
    @staticmethod
    def lerp(start, end, proportion):
        return round(start + (end - start) * proportion, 3)

    @staticmethod
    def invert_two_digit(digit):
        return -digit[0], -digit[1]


# class ScaledSurface:
#     def __init__(self, width, height):
#         self.width = width * 2
#         self.height = height * 2
#         self.temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
#         self.center = (width, height)
#
#     def add(self, space_obj):
#         from .ships import BaseShip
#
#         sprite = space_obj.sprite
#         if isinstance(space_obj, BaseShip):
#             sprite = space_obj.current_sprite
#
#         correct_position = (
#             self.center[0] + (space_obj.body.position.x - self.center[0]),
#             self.center[1] + (space_obj.body.position.y - self.center[1])
#         )
#
#         rect = sprite.get_rect(center=correct_position)
#         self.temp_surface.blit(sprite, rect.topleft)
#
#     def draw_on_screen(self, screen):
#         scaled_surface = pygame.transform.scale(
#             self.temp_surface,
#             (int(self.width * config.ZOOM), int(self.height * config.ZOOM))
#         )
#
#         scaled_rect = scaled_surface.get_rect(center=screen.get_rect().center)
#         screen.blit(scaled_surface, scaled_rect)


class PhysicalSpace:
    def __init__(self):
        self.space = pymunk.Space()
        self.handler = self.space.add_collision_handler(1, 1)
        self.handler.begin = self.damage_handler

    def add(self, obj):
        self.space.add(obj.body, obj.get_shape())

    def remove(self, objs):
        self.space.remove(objs.body, objs.shape)

    def move(self, camera_position):
        for body in self.space.bodies:
            body.position += camera_position

    def get_simulation_step(self):
        return self.space.step(1 / config.FPS)

    @staticmethod
    def get_collision_data(arbiter):
        body_a, body_b = arbiter.shapes[0].body, arbiter.shapes[1].body
        velocity_a = body_a.velocity
        velocity_b = body_b.velocity
        angular_velocity_a = body_a.angular_velocity
        angular_velocity_b = body_b.angular_velocity
        center_mass_a = body_a.position
        center_mass_b = body_b.position
        return velocity_a, velocity_b, angular_velocity_a, angular_velocity_b, center_mass_a, center_mass_b

    @staticmethod
    def calculate_relative_velocity(velocity_a, velocity_b, angular_velocity_a, angular_velocity_b, contact_point,
                                    center_mass_a, center_mass_b):
        ra = contact_point - center_mass_a
        rb = contact_point - center_mass_b
        velocity_a_contact = velocity_a + angular_velocity_a * ra.perpendicular()
        velocity_b_contact = velocity_b + angular_velocity_b * rb.perpendicular()
        relative_velocity = velocity_a_contact - velocity_b_contact
        return relative_velocity

    @staticmethod
    def calculate_collision_force(relative_velocity, mass_a, mass_b):
        # Расчёт силы столкновения
        relative_speed = relative_velocity.length
        combined_mass = mass_a * mass_b / (mass_a + mass_b)
        collision_force = combined_mass * relative_speed
        return collision_force

    @staticmethod
    def calculate_damage(collision_force):
        # Простой пример расчета урона
        damage = collision_force * config.DAMAGE  # Коэффициент для регулирования урона
        return damage

    def damage_handler(self, arbiter, space, data):
        # Извлекаем данные о столкновении
        (velocity_a, velocity_b, angular_velocity_a, angular_velocity_b, center_mass_a,
         center_mass_b) = self.get_collision_data(arbiter)

        # Берем первую точку контакта для простоты
        contact_point = arbiter.contact_point_set.points[0].point_a

        # Рассчитываем относительную скорость
        relative_velocity = self.calculate_relative_velocity(velocity_a, velocity_b, angular_velocity_a,
                                                             angular_velocity_b,
                                                             contact_point, center_mass_a, center_mass_b)

        # Получаем массы объектов
        mass_a = arbiter.shapes[0].body.mass
        mass_b = arbiter.shapes[1].body.mass

        # Рассчитываем силу столкновения
        collision_force = self.calculate_collision_force(relative_velocity, mass_a, mass_b)

        # Рассчитываем урон
        damage = self.calculate_damage(collision_force)

        # Здесь вы можете обновить здоровье объектов или вызвать другие эффекты столкновения
        arbiter.shapes[0].object_data.take_damage(damage)
        arbiter.shapes[1].object_data.take_damage(damage)

        return True


class BaseSpaceBG:
    def __init__(self, surface, image_path, bg_color=None):
        self.surface = surface
        self.x = self.y = 0
        self.image = pygame.image.load(image_path).convert_alpha()
        if bg_color:
            self.bg_color = pygame.Surface((config.WIDTH, config.HEIGHT))
            self.bg_color.fill(bg_color)

    def draw(self, camera, speed_factor):
        camera_offset = camera.camera.topleft
        self.update_coordinates(camera_offset, speed_factor)
        if hasattr(self, 'bg_color'):
            self.surface.blit(self.bg_color, (0, 0))
            self.blit_repeated_background()
        else:
            self.surface.blit(self.image, (self.x, self.y))

    def update_coordinates(self, coord, speed_factor):
        self.x = -coord[0] * speed_factor
        self.y = -coord[1] * speed_factor
        self.wrap_coordinates()

    def wrap_coordinates(self):
        if hasattr(self, 'bg_color'):
            if -config.WIDTH >= self.x or self.x >= config.WIDTH:
                self.x = 0
            if -config.HEIGHT >= self.y or self.y >= config.HEIGHT:
                self.y = 0

    def blit_repeated_background(self):
        # for dx in [-config.WIDTH, 0, config.WIDTH]:
        #     for dy in [-config.HEIGHT, 0, config.HEIGHT]:
        #         self.surface.blit(self.image, (self.x + dx, self.y + dy))y

        self.surface.blit(self.bg_color, (0, 0))

        self.surface.blit(self.image, (self.x, self.y))
        self.surface.blit(self.image, (self.x, self.y - config.HEIGHT))
        self.surface.blit(self.image, (self.x, self.y + config.HEIGHT))
        self.surface.blit(self.image, (self.x - config.WIDTH, self.y))
        self.surface.blit(self.image, (self.x + config.WIDTH, self.y))
        self.surface.blit(self.image, (self.x - config.WIDTH, self.y - config.HEIGHT))
        self.surface.blit(self.image, (self.x + config.WIDTH, self.y + config.HEIGHT))
        self.surface.blit(self.image, (self.x - config.WIDTH, self.y + config.HEIGHT))
        self.surface.blit(self.image, (self.x + config.WIDTH, self.y - config.HEIGHT))


class SpaceBG(BaseSpaceBG):
    def __init__(self, surface):
        super().__init__(surface, 'images/space/background/stars.png', bg_color=(33, 9, 74))

    def draw(self, camera, **kwargs):
        super().draw(camera, speed_factor=0.4)


class SpaceBGPlanets(BaseSpaceBG):
    def __init__(self, surface):
        super().__init__(surface, 'images/space/space_objects/planets/planet2.png')

    def draw(self, camera, **kwargs):
        super().draw(camera, speed_factor=0.6)


class SpaceObject:
    """
    collision_type = 1 - Космический мусор
    """
    MASS = 1
    ELASTICITY = 0
    FRICTION = 0

    HEALTH = 1

    SPRITE_PATH = None

    def __init__(self, position, body_type='circle'):
        self.health = self.HEALTH

        self._sprite = pygame.image.load(self.SPRITE_PATH).convert_alpha()
        self.current_sprite = self._sprite
        self.overlay_sprites_list = []

        self.original_radius = self._sprite.get_rect().width // 2
        self.radius = self.original_radius

        self.original_mass = self.MASS
        self.mass = self.MASS

        if body_type == 'circle':
            self.body = pymunk.Body(self.mass, pymunk.moment_for_circle(self.mass, 0, self.radius))
            self.body.type = 'circle'
        elif body_type == 'box':
            self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, self._sprite.get_size()))
            self.body.type = 'box'
        self.body.position = position

        self.shape = None

    def get_circle_shape(self):
        circle_shape = pymunk.Circle(self.body, self.radius)
        circle_shape.elasticity = self.ELASTICITY
        circle_shape.friction = self.FRICTION
        circle_shape.collision_type = 1
        circle_shape.object_data = self
        return circle_shape

    def get_box_shape(self):
        box_shape = pymunk.Poly.create_box(self.body, self._sprite.get_size())
        box_shape.elasticity = self.ELASTICITY
        box_shape.collision_type = 1
        box_shape.object_data = self
        return box_shape

    def get_shape(self):
        if self.body.type == 'circle':
            self.shape = self.get_circle_shape()
        elif self.body.type == 'box':
            self.shape = self.get_box_shape()
        return self.shape

    def overlay_sprites(self, sprites):
        if not sprites:
            return self._sprite
        elif len(sprites) == 1:
            return sprites[0]

        # Определяем размер результирующего изображения
        result_width = max(sprite.get_width() for sprite in sprites)
        result_height = max(sprite.get_height() for sprite in sprites)
        result_image = pygame.Surface((result_width, result_height), pygame.SRCALPHA)

        # Накладываем спрайты друг на друга
        for sprite in sprites:
            result_image.blit(sprite, (0, 0))

        sprites.clear()
        return result_image

    def draw(self, surface, camera):
        self.current_sprite = self.overlay_sprites(self.overlay_sprites_list)

        sprite = self.rotate_sprite()
        position = camera.apply(self.body.position)
        rect = sprite.get_rect(center=position)
        surface.blit(sprite, rect.topleft)

    def rotate_sprite(self):
        return pygame.transform.rotate(self.current_sprite, -math.degrees(self.body.angle))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            object_destruction_event = pygame.event.Event(events.OBJECT_DESTRUCTION, object=self)
            pygame.event.post(object_destruction_event)


class Meteorite(SpaceObject):
    MASS = 500
    ELASTICITY = 0.5
    FRICTION = 1
    SPRITE_PATH = 'images/space/space_objects/meteorites/meteorite_roma-test.png'

    HEALTH = 100


class Meteorite2(SpaceObject):
    MASS = 1000
    ELASTICITY = 0.5
    FRICTION = 1
    SPRITE_PATH = 'images/space/space_objects/meteorites/meteorite_roma-test2.png'

    HEALTH = 100
