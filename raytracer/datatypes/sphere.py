from math import sqrt
from .ray import Ray

class Sphere:
    """Represents a 3D sphere with ray intersection capabilities.
    
    Implements:
    - Ray-sphere intersection testing
    - Surface normal calculation
    - Material association for rendering
    
    Mathematical Basis:
    Sphere Equation: (x - c_x)^2 + (y - c_y)^2 + (z - c_z)^2 = r^2
    Ray Equation: p(t) = o + t*d
    Combined Equation: t^2(d·d) + 2t(d·(o-c)) + (o-c)·(o-c) - r^2 = 0
    """

    def __init__(self, center, radius, material):
        """Initialize sphere with geometric and material properties.
        
        Args:
            center (Point): 3D coordinates of sphere center (x, y, z)
            radius (float): Sphere radius (> 0)
            material (Material): Surface material properties
        """
        self.center = center    # Sphere's center point in 3D space
        self.radius = radius    # Sphere's radius (must be positive)
        self.material = material  # Surface material for shading

    def intersects(self, ray: Ray):
        # Quadratic equation components visualization
        #        ray origin
        #           o
        #           |\ 
        #           | \ direction
        #           |  \
        #           |   \
        # center c •|----•---> closest intersection
        #           |     \
        #           |      sphere surface
        #           |
        """Calculate ray-sphere intersection using geometric solution.
        
        Args:
            ray (Ray): Ray to test for intersection
            
        Returns:
            float: Distance along ray to nearest intersection
            None: If no valid intersection exists
        """
        # Vector from sphere center to ray origin
        sphere_to_ray = ray.org - self.center        
        # Calculate quadratic equation coefficients
        # Simplified form assumes normalized ray direction (||d|| = 1)
        # a = 1 (omitted from calculation)
        b = 2 * ray.dir.dot_product(sphere_to_ray.data)  # 2*(d·(o-c))
        c = sphere_to_ray.dot_product(sphere_to_ray.data) - self.radius * self.radius  # ||o-c||² - r²
        
        discriminant = b * b - 4 * c  # b² - 4ac (a=1)

        # No intersection if discriminant negative
        if discriminant < 0:
            return None

        # Calculate both roots
        sqrt_discriminant = sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / 2  # Closer intersection
        t2 = (-b + sqrt_discriminant) / 2  # Farther intersection

        # Return smallest positive solution
        if t1 > 0:
            return t1
        if t2 > 0:
            return t2
        return None

    def normal(self, surface_point):
        # Normal vector visualization
        #           surface_point
        #                 •
        #                /|
        #               / |
        #              /  |
        #             /   |
        #            /    |
        # center c •<-----• normal
        """Calculate unit normal vector at surface point.
        
        Args:
            surface_point (Point): Point on sphere surface
            
        Returns:
            Vector: Unit normal pointing outward from sphere
        """
        # Normal vector points from center to surface point
        raw_normal = surface_point - self.center
        
        # Normalize to unit length for proper lighting calculations
        return raw_normal.normalize