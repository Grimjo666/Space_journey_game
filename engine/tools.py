from decimal import Decimal
import pymunk


class ToolMixin:
    ROUNDING_DEGREE = Decimal("1.0000")

    def round(self, num, rounding_degree=None):
        if not rounding_degree:
            rounding_degree = self.ROUNDING_DEGREE
        return Decimal(num).quantize(rounding_degree)

    def round_vec(self, vec):
        x = self.round(vec[0])
        y = self.round(vec[1])

        return pymunk.Vec2d(x, y)