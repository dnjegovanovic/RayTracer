from .vector import Vector


class Color(Vector):
    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0):
        super().__init__()
        self.r = r  # Uses __setattr__
        self.g = g
        self.b = b

    def __setattr__(self, name, value):
        if name in ("r", "g", "b"):
            # Map color components to vector coordinates
            coord = {"r": "x", "g": "y", "b": "z"}[name]
            super().__setattr__(coord, value)
        else:
            super().__setattr__(name, value)

    @property
    def r(self):
        return self.x

    @property
    def g(self):
        return self.y

    @property
    def b(self):
        return self.z

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)
