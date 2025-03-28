from .color import Color


class Material:
    def __init__(
        self,
        color: Color = Color.from_hex("#FFFFFF"),
        ambient: float = 0.05,
        diffuse: float = 1.0,
        specular: float = 1.0,
        reflection: float = 0.5,
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, hit_pos):
        return self.color


class ChequerMaterial:
    def __init__(
        self,
        color1: Color = Color.from_hex("#FFFFFF"),
        color2: Color = Color.from_hex("#000000"),
        ambient: float = 0.05,
        diffuse: float = 1.0,
        specular: float = 1.0,
        reflection: float = 0.5,
    ):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, position):
        if int((position.x + 5.0) * 3.0) % 2 == int((position.z * 3.0)) % 2:
            return self.color1
        else:
            return self.color2
