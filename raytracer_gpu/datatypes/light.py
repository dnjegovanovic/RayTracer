from .point import Point
from .color import Color


class PointLight:
    def __init__(self, position: Point, color: Color = Color.from_hex("#FFFFFF")):
        """_summary_

        Args:
            position (Point): position of light
            color (Color, optional): Light color. Defaults to Color.from_hex("#FFFFFF").
        """
        self.positions = position
        self.color = color
