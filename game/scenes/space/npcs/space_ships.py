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
            # NeutralShip((600, 500)),
            # NeutralShip((400, 1000)),
            # NeutralShip((400, 1600)),
            # NeutralShip((1800, 1000)),
            # NeutralShip((2000, 1500)),
            # NeutralShip((2000, 1800)),
            # NeutralShip((600, 1500)),
            # NeutralShip((500, 1500)),
            # NeutralShip((3000, 1800)),
            # NeutralShip((600, 1500)),
        )

        super().__init__(ships)
