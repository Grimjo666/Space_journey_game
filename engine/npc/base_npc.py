import pygame

from engine.npc import behaviors


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

    def draw(self, screen, camera):
        self.ship.draw(screen, camera)


class BaseNPCManager:
    def __init__(self, npc_arr):
        self.NPCs = npc_arr

    def update(self):
        for npc in self.NPCs:
            if npc.current_behavior is None:
                npc.set_behavior()
            npc.update()

    def draw(self, screen, camera):
        for npc in self.NPCs:
            npc.draw(screen, camera)

    def get_npc(self):
        return self.NPCs
