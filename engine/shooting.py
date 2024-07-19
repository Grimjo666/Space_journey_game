from engine.space import SpaceObject

from game import config


class BaseBullet(SpaceObject):
    OBJECT_TYPE = 'bullet'

    SPRITE_PATH = 'game/images/space/bullets/base_bullet.png'

    MASS = 1
    ELASTICITY = 0.5
    FRICTION = 1

    HEALTH = 1

    def __init__(self, position, angle, damage):
        super().__init__(position)
        self.body.moment = float('inf')
        self.body.angle = angle

        self.damage = damage


class BaseWeapon:
    BULLET_TYPE = BaseBullet

    SHOT_SPEED = 5
    SHOT_DELAY_MULTIPLIER = 0.1  # Задержка в секундах
    DAMAGE = 100

    def __init__(self, position, angle):
        self.bullet = self.BULLET_TYPE(position, angle, damage=self.DAMAGE)
        self.bullet_list = []
        self.shot_delay = 0

    def shot(self, target_position):
        impulse = target_position * self.SHOT_SPEED
        if self.bullet.body.velocity.length == 0:
            self.bullet.body.apply_impulse_at_world_point(impulse, (0, 0))

    def update(self, position, angle, parent):
        """
        Обновляем данные пушки (создаём новую пулю)
        :param position: позиция для пули
        :param angle: угол наклона пули
        :param parent: экземпляр класса корабля, сделавшего выстрел
        :return:
        """
        # Создаём пулю
        self.bullet = self.BULLET_TYPE(position, angle, damage=self.DAMAGE)
        self.bullet_list.append(self.bullet)

        # связываем выстрел с кораблём-родителем
        self.bullet.parent_id = id(parent)

    def get_bullet(self):
        if self.bullet_list:
            return self.bullet_list.pop()
