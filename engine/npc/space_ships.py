import pygame

from engine.npc import behaviors
import engine.ships


class BaseShipNPC:
    BEHAVIORS = {
        'patrolling': behaviors.BasePatrolling,
    }
    SHIP = None

    def __init__(self, position):
        self.ship = self.SHIP(position)
        self.state = 'patrolling'
        self.current_behavior = None

    def set_behavior(self):
        self.current_behavior = self.BEHAVIORS[self.state](self.ship)

    def update(self):
        self.current_behavior.update()


class NeutralShip(BaseShipNPC):
    SHIP = engine.ships.Cruiser

    def __init__(self, position):
        super().__init__(position)


class SpaceShipNPCManager:
    def __init__(self, ships):
        self.ships = ships

    def update(self):
        for ship in self.ships:
            if ship.currnt_behavior is None:
                ship.set_behavior()
            ship.update()

    def draw(self):
        pass
