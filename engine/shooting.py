from engine.space import SpaceObject

from game import config


class BaseBullet(SpaceObject):
    OBJECT_TYPE = 'bullet'

    SPRITE_PATH = 'game/images/space/bullets/base_bullet.png'

    MASS = 1
    ELASTICITY = 0.5
    FRICTION = 1

    HEALTH = 1
    SHOOT_SPEED = 5

    DAMAGE = 100

    def __init__(self, position, angle):
        super().__init__(position)
        self.body.moment = float('inf')
        self.body.angle = angle

    def shot(self, target_position):
        impulse = target_position * self.SHOOT_SPEED
        if self.body.velocity.length == 0:
            self.body.apply_impulse_at_world_point(impulse, (0, 0))
