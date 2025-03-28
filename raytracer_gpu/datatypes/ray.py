from raytracer.datatypes.vector import Vector


class Ray:
    """Ray with an oirigin and norm direction"""

    def __init__(self, origin: Vector, direction: Vector):
        self.org = origin
        self.dir = direction.normalize
