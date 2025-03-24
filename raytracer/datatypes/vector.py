import numpy as np


class Vector:
    """Simple vector with 3 element based on numpy"""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        # Use direct assignment to avoid triggering __setattr__ during init
        super().__setattr__("x", x)
        super().__setattr__("y", y)
        super().__setattr__("z", z)
        super().__setattr__("data", np.array([x, y, z], dtype=np.float32))

    def __setattr__(self, name, value):
        if name in ("x", "y", "z"):
            # Update both the coordinate and the numpy array
            super().__setattr__(name, value)
            new_data = np.array([self.x, self.y, self.z], dtype=np.float32)
            super().__setattr__("data", new_data)
        else:
            super().__setattr__(name, value)

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

    @property
    def mag(self):
        return np.linalg.norm(self.data)

    def dot_product(self, sec_vec) -> np.float32:
        return np.dot(self.data, sec_vec)

    @property
    def normalize(self):
        return Vector(self.x / self.mag, self.y / self.mag, self.z / self.mag)

    def __add__(self, sec_vec):
        return Vector(self.x + sec_vec.x, self.y + sec_vec.y, self.z + sec_vec.z)

    def __sub__(self, sec_vec):
        if isinstance(sec_vec, Vector):
            return Vector(self.x - sec_vec.x, self.y - sec_vec.y, self.z - sec_vec.z)
        else:
            return Vector(self.x - sec_vec, self.y - sec_vec, self.z - sec_vec)

    def __mul__(self, number):
        assert not isinstance(number, Vector)
        return Vector(
            self.data[0] * number, self.data[1] * number, self.data[2] * number
        )

    def __rmul__(self, number):
        return self.__mul__(number)

    def __truediv__(self, number):
        assert not isinstance(number, Vector)
        nv = self.data / number
        return Vector(nv[0], nv[1], nv[2])
