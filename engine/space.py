import math

import pygame
import pymunk

from game import config

from engine import events, scene

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


OBJECTS_TYPES = {
    'any': 0,
    'player': 1,
    'friend': 2,
    'enemy': 3,
    'cosmic_body': 4,
    'bullet': 5
}


class PhysicalSpace:
    def __init__(self):
        self.space = pymunk.Space()

        # Регистрация обработчика коллизий для всех нужных типов объектов
        for type_a in OBJECTS_TYPES.values():
            for type_b in OBJECTS_TYPES.values():
                self.space.add_collision_handler(type_a, type_b).begin = self.collision_handler

    def add(self, obj):
        self.space.add(obj.body, obj.get_shape())

        # Если у объекта есть родитель, то добавляем его в группу с родителем
        if obj.parent_id:
            obj.shape.filter = pymunk.ShapeFilter(group=obj.parent_id)
        else:
            obj.shape.filter = pymunk.ShapeFilter(group=id(obj))

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

    def collision_handler(self, arbiter, space, data):
        """
        Обработчик столкновений в физическом пространстве игры.
        Определяет тип сталкивающихся объектов и вызывает обработчики столкновений
        :param arbiter:
        :param space:
        :param data:
        :return:
        """

        shape_a, shape_b = arbiter.shapes
        type_a = shape_a.collision_type
        type_b = shape_b.collision_type

        any_obj = OBJECTS_TYPES['any']
        player = OBJECTS_TYPES['player']
        bullet = OBJECTS_TYPES['bullet']

        # Если среди объектов есть снаряд
        if bullet in (type_a, type_b):

            # Если среди объектов только один снаряд
            if not all((type_a == bullet, type_b == bullet)):
                # Обрабатываем коллизию пули с любым другим объектом
                self.handle_any_and_bullet_collision(shape_a, shape_b)
            else:
                print('Добавь обработку bullet X bullet')

        elif player in (type_a, type_b):
            self.handle_player_and_any_collision(arbiter)

        else:
            self.handle_any_collision(arbiter)

        return True

    def handle_any_collision(self, arbiter):
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

        # Наносим урон объектам
        arbiter.shapes[0].object_data.take_damage(damage)
        arbiter.shapes[1].object_data.take_damage(damage)

    def handle_player_and_any_collision(self, arbiter):
        self.handle_any_collision(arbiter)

    @staticmethod
    def handle_any_and_bullet_collision(shape_a, shape_b):
        from engine.shooting import BaseBullet
        obj_a, obj_b = shape_a.object_data, shape_b.object_data

        # Поверяем какой из объектов является выстрелом и берём его урон
        if isinstance(obj_a, BaseBullet):
            damage = obj_a.damage
        else:
            damage = obj_b.damage

        # Наносим урон объектам
        obj_a.take_damage(damage)
        obj_b.take_damage(damage)


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


class SpaceObject:
    OBJECT_TYPE = 'any'

    MASS = 1
    ELASTICITY = 0
    FRICTION = 0

    HEALTH = 1

    SPRITE_PATH = None

    def __init__(self, position, body_type='circle'):
        self.health = self.HEALTH
        self.health_view_time_counter = 0

        self._sprite = pygame.image.load(self.SPRITE_PATH).convert_alpha()
        self.current_sprite = self._sprite
        self.overlay_sprites_list = []

        self.width = self._sprite.get_width()
        self.height = self._sprite.get_height()

        self.original_mass = self.MASS
        self.mass = self.MASS

        if body_type == 'circle':
            self.original_radius = self._sprite.get_rect().width // 2
            self.radius = self.original_radius

            self.body = pymunk.Body(self.mass, pymunk.moment_for_circle(self.mass, 0, self.radius))
            self.body.type = 'circle'
        elif body_type == 'box':
            self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, self._sprite.get_size()))
            self.body.type = 'box'
        self.body.position = position

        self.shape = None

        self.parent_id = None

    def get_circle_shape(self):
        circle_shape = pymunk.Circle(self.body, self.radius)
        circle_shape.elasticity = self.ELASTICITY
        circle_shape.friction = self.FRICTION
        circle_shape.collision_type = OBJECTS_TYPES[self.OBJECT_TYPE]
        circle_shape.object_data = self
        return circle_shape

    def get_box_shape(self):
        box_shape = pymunk.Poly.create_box(self.body, self._sprite.get_size())
        box_shape.elasticity = self.ELASTICITY
        box_shape.collision_type = OBJECTS_TYPES[self.OBJECT_TYPE]
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

        # Рисуем шкалу здоровья, если объект не игрок или снаряд
        if self.health_view_time_counter != 0 and self.OBJECT_TYPE not in ('bullet', 'player'):
            self.draw_health_bar(surface, camera)
            self.health_view_time_counter -= 1

    def rotate_sprite(self):
        return pygame.transform.rotate(self.current_sprite, -math.degrees(self.body.angle))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            object_destruction_event = pygame.event.Event(events.OBJECT_DESTRUCTION, object=self)
            pygame.event.post(object_destruction_event)

        self.health_view_time_counter = config.FPS * config.VIEW_HEALTH_BAR_TIME

    def draw_health_bar(self, screen, camera):
        # Вычисляем позицию health bar с учётом размеров объекта
        x = self.body.position[0] - self.width / 2
        y = self.body.position[1] - self.height / 2

        # Корректируем позицию относительно смещения камеры
        position = camera.apply((x, y))

        # Рассчитываем ширину внутреннего заполнения
        fill_width = int(150 * (self.health / self.HEALTH))

        # Рисуем внутреннее заполнение
        pygame.draw.rect(screen, 'Red', (*position, fill_width, 10))
        # Рисуем обводку
        pygame.draw.rect(screen, 'Yellow', (*position, 150, 10), 2)


class BaseShip(SpaceObject):
    MAX_SPEED = 0
    ENGINE_POWER = 0

    # Параметры ниже выставляются в градусах
    ROTATE_SPEED = 0
    ROTATE_SLOWDOWN_THRESHOLD = 0
    MIN_ROTATE_SPEED = 0

    BASE_WEAPON = None

    def __init__(self, ship_position, body_type='circle'):
        super().__init__(ship_position, body_type)

        self.rotate_speed = math.radians(self.ROTATE_SPEED * config.FPS_FACTOR)
        self.rotate_slowdown_threshold = math.radians(self.ROTATE_SLOWDOWN_THRESHOLD)
        self.min_rotate_speed = math.radians(self.MIN_ROTATE_SPEED * config.FPS_FACTOR)

        self._accelerator_sprites = None
        self._rotate_left_sprites = None
        self._rotate_right_sprites = None
        self.motion_sprite_counter = -1
        self.rotate_point = self.body.position

        self.first_weapon = self.BASE_WEAPON(self.body.position, self.body.angle)

    def update_rotate_point(self, camera=None):
        if camera:
            self.rotate_point = camera.apply(self.body.position)
        else:
            self.rotate_point = self.body.position

    def update(self, camera=None):
        self.update_rotate_point(camera)
        self.first_weapon.shot_delay -= 1

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

        return pymunk.Vec2d(dx, dy)

    def smooth_rotation(self, target_angle=None):
        """
        Метод должен вызываться после всех действий с перемещением корабля
        :param target_angle:
        :return:
        """
        self.add_rotate_animation(target_angle)

        # Логика поворота с симуляцией массы корабля
        if not target_angle:
            target_angle = self.calculate_angle()

        current_angle = self.body.angle
        difference = target_angle - current_angle

        if abs(difference) <= 0.08:
            difference = 0

        if difference > math.pi:
            difference -= 2 * math.pi
        elif difference < -math.pi:
            difference += 2 * math.pi

        # Замедление в конце поворота
        if abs(difference) < self.rotate_slowdown_threshold:
            rotate_speed = max(self.min_rotate_speed,
                               self.rotate_speed * abs(difference) // self.rotate_slowdown_threshold)
        else:
            rotate_speed = self.rotate_speed

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
        self.add_accelerator_animation()

        if scene.FPS_STEP_COUNTER == 0:
            impulse = self.get_movement_vector() * self.ENGINE_POWER
            self.body.apply_impulse_at_world_point(impulse, (0, 0))
        self.limit_velocity()

    def deceleration_ship(self):
        if self.body.velocity.length < self.MAX_SPEED * 0.1:
            self.body.velocity = pymunk.Vec2d(0, 0)
        elif scene.FPS_STEP_COUNTER == 0:
            self.body.velocity *= 0.95

    def limit_velocity(self):
        if self.body.velocity.length > self.MAX_SPEED:
            self.body.velocity = self.body.velocity.normalized() * self.MAX_SPEED

    def rotate_sprite(self):
        return pygame.transform.rotate(self.current_sprite, -math.degrees(self.body.angle) - 90)

    def add_accelerator_animation(self):
        if scene.FPS_STEP_COUNTER == 0:
            self.motion_sprite_counter += 1
            if self.motion_sprite_counter == 4:
                self.motion_sprite_counter = 0

        self.overlay_sprites_list.append(self._accelerator_sprites[self.motion_sprite_counter])

    def add_rotate_animation(self, target_angle=None):

        if not target_angle:
            target_angle = self.calculate_angle()

        difference = target_angle - self.body.angle

        if abs(difference) <= 0.08:
            difference = 0

        if difference > math.pi:
            difference -= 2 * math.pi
        elif difference < -math.pi:
            difference += 2 * math.pi

        # Если разница в углах больше, то вычисляем направление вращения
        if abs(difference) > math.radians(0.5):
            if difference < 0:
                if scene.FPS_STEP_COUNTER == 0:  # настраиваем скорость анимации
                    self.motion_sprite_counter = (self.motion_sprite_counter + 1) % len(self._rotate_left_sprites)
                self.overlay_sprites_list.append(self._rotate_left_sprites[self.motion_sprite_counter])
            else:
                if scene.FPS_STEP_COUNTER == 0:  # настраиваем скорость анимации
                    self.motion_sprite_counter = (self.motion_sprite_counter + 1) % len(self._rotate_right_sprites)
                self.overlay_sprites_list.append(self._rotate_right_sprites[self.motion_sprite_counter])
        else:
            self.overlay_sprites_list.append(self._sprite)

    def inactivity_animation(self):
        self.current_sprite = self._sprite

    def ship_control(self, keys, mouse_keys, target_angle=None):

        # движение по нажатию на кнопку W
        if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
            self.move_ship()  # Активируем движение корабля
            # ускорение
            if keys[pygame.K_LALT]:
                pass

        # Выстрел по нажатию на правую кнопку мыши с учётом задержки орудия
        if mouse_keys[2] and self.first_weapon.shot_delay <= 0:
            self.take_shot()

            # Включаем задержку
            self.first_weapon.shot_delay = config.FPS * self.first_weapon.SHOT_DELAY_MULTIPLIER

        elif keys[pygame.K_SPACE]:
            self.deceleration_ship()  # Активируем торможение корабля

        self.smooth_rotation(target_angle)  # Активируем вращение корабля

    def take_shot(self):
        """
         Метод для стрельбы корабля
        """
        # Обновляем объект-пушку
        self.first_weapon.update(self.body.position, self.body.angle, self)
        # Стреляем
        self.first_weapon.shot(self.get_movement_vector())
