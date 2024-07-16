from engine.space import BaseSpaceBG


class SpaceBG(BaseSpaceBG):
    def __init__(self, surface):
        super().__init__(surface, 'game/images/space/background/stars.png', bg_color=(33, 9, 74))

    def draw(self, camera, **kwargs):
        super().draw(camera, speed_factor=0.4)


class SpaceBGPlanets(BaseSpaceBG):
    def __init__(self, surface):
        super().__init__(surface, 'game/images/space/space_objects/planets/saturn.png')

    def draw(self, camera, **kwargs):
        super().draw(camera, speed_factor=0.6)