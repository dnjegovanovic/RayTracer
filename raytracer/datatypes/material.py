from .color import Color


class Material:
    def __init__(
        self,
        color: Color = Color.from_hex("#FFFFFF"),
        ambient: float = 0.05,
        diffuse: float = 1.0,
        specular: float = 1.0,
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def color_at(self, hit_pos):
        return self.color
