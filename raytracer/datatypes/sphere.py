from math import *
from .ray import Ray


class Sphere:
    """Sphere is the 3D shape implemented."""

    def __init__(self, center, radius, material):
        """_summary_

        Args:
            center (_type_): center of sphere (x,y)
            radius (_type_): sphere radius
            material (_type_): materisl (u,v)
        """
        self.center = center
        self.radius = radius
        self.material = material

    def intersects(self, ray: Ray):
        """Checks if the ray intesects with spehere.
           Return distance to intersec or None if there is no inters

        Args:
            ray (_type_): _description_
        """

        # a = 1
        sphere_to_ray = ray.org - self.center
        b = 2 * ray.dir.dot_product(sphere_to_ray.data)
        c = sphere_to_ray.dot_product(sphere_to_ray.data) - self.radius * self.radius
        discriminant = b * b - 4 * c

        if discriminant >= 0.0:
            dist = (-b - sqrt(discriminant)) / 2
            if dist > 0:
                return dist
        return None

    def normal(self, surface_point):
        """Return the normal to the point on the sphere surface

        Args:
            surface_point (_type_): _description_
        """

        return (surface_point - self.center).normalize
