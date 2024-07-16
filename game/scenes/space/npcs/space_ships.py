from engine.npc.base_npc import BaseShipNPC, BaseNPCManager

from game.scenes.space.ship_templates import Cruiser


class NeutralShip(BaseShipNPC):
    SHIP = Cruiser

    def __init__(self, position):
        super().__init__(position)


class ShipsNPCManager(BaseNPCManager):

    def __init__(self):

        ships = (
            NeutralShip((200, 500)),
            NeutralShip((200, 800)),
            NeutralShip((600, 500)),
        )

        super().__init__(ships)
