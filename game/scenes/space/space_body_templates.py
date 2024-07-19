from engine.space import SpaceObject


class Meteorite(SpaceObject):
    OBJECT_TYPE = 'cosmic_body'

    MASS = 500
    ELASTICITY = 0.5
    FRICTION = 1
    SPRITE_PATH = 'game/images/space/space_objects/meteorites/meteorite_roma-test.png'

    HEALTH = 100


class Meteorite2(SpaceObject):
    OBJECT_TYPE = 'cosmic_body'

    MASS = 1000
    ELASTICITY = 0.5
    FRICTION = 1
    SPRITE_PATH = 'game/images/space/space_objects/meteorites/meteorite_roma-test2.png'

    HEALTH = 500


class SpaceSnot(SpaceObject):
    OBJECT_TYPE = 'cosmic_body'

    MASS = 100
    ELASTICITY = 0.8
    FRICTION = 1
    SPRITE_PATH = 'game/images/space/space_objects/meteorites/space_snot.png'
