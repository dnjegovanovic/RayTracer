import numpy as np


class Vector:
    """Simple vector with 3 element based on numpy"""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.data = np.array([self.x, self.y, self.z], dtype=np.float32)

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

    @property
    def mag(self):
        return np.linalg.norm(self.data)

    def dot_product(self, sec_vec: np.array) -> np.float32:
        return np.dot(self.data, sec_vec)

    @property
    def normalize(self):
        return self.data / self.mag

    def __add__(self, sec_vec):
        return Vector(self.x + sec_vec.x, self.y + sec_vec.y, self.z + sec_vec.z)

    def __sub__(self, sec_vec):
        return Vector(self.x - sec_vec.x, self.y - sec_vec.y, self.z - sec_vec.z)

    def __mul__(self, number):
        assert not isinstance(number, Vector)
        nv = self.data * number
        return Vector(nv[0], nv[1], nv[2])

    def __rmul__(self, number):
        return self.__mul__(number)

    def __truediv__(self, number):
        assert not isinstance(number, Vector)
        nv = self.data / number
        return Vector(nv[0], nv[1], nv[2])
