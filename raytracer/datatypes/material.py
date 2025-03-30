from .color import Color


# Ambient: I_a = k_a * i_a (constant ambient light contribution)
# Diffuse: I_d = k_d * (N·L) * i_d (lambertian cosine law)
# Specular: I_s = k_s * (N·H)^α * i_s (blinn-phong approximation)
# Where:
# - N: Surface normal
# - L: Light direction
# - H: Half vector between view and light
# - α: Specular exponent (hard-coded elsewhere as 50)
class Material:
    """Base material class implementing Phong reflection model components.

    The Phong reflection model: I = I_ambient + I_diffuse + I_specular
    Where:
    - Ambient: Constant lighting approximation
    - Diffuse: Lambertian cosine law for matte surfaces
    - Specular: Blinn-Phong approximation for shiny highlights

    Args:
        color (Color): Base color of material (RGB)
        ambient (float): Ambient reflection coefficient (0-1)
        diffuse (float): Diffuse reflection coefficient (0-1)
        specular (float): Specular reflection coefficient (0-1)
        reflection (float): Mirror-like reflection strength (0-1)
    """

    def __init__(
        self,
        color: Color = Color.from_hex("#FFFFFF"),
        ambient: float = 0.05,  # Typical ambient value for minimal lighting
        diffuse: float = 1.0,  # Full diffuse response
        specular: float = 1.0,  # Full specular highlights
        reflection: float = 0.5,  # Semi-reflective surface
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, hit_pos):
        """Returns constant color regardless of position"""
        return self.color


# The formula creates alternating tiles using integer division:
# pattern = parity of (floor(scaled_x) XOR floor(scaled_z))
#
# Visual representation when frequency=3:
# [x+z] % 2 = 0: color1    [x+z] % 2 = 1: color2
# -------------------------
# | color1 | color2 | color1 |
# -------------------------
# | color2 | color1 | color2 |
# -------------------------
# | color1 | color2 | color1 |
# -------------------------
class ChequerMaterial:
    """Checkerboard pattern material using modular arithmetic for pattern generation.

    Pattern formula:
    Given position (x, y, z), creates checkers using:
    pattern = (floor((x + offset) * frequency) % 2 == floor(z * frequency) % 2

    Design choices:
    - Offset (5.0): Shifts pattern to avoid origin symmetry issues
    - Frequency (3.0): Controls checker density (higher = more tiles)
    - XZ plane: Common choice for ground plane patterns
    """

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
        """Calculates checker pattern using discretized position coordinates.

        Args:
            position (Point): 3D hit position in world coordinates

        Returns:
            Color: Selected color based on checkerboard pattern
        """
        # Pattern generation parameters
        offset = 5.0  # Avoids negative coordinate issues
        frequency = 3.0  # Controls number of checkers per unit space

        # Discretize coordinates and check parity
        x_pattern = int((position.x + offset) * frequency) % 2
        z_pattern = int(position.z * frequency) % 2

        # Alternate colors based on combined pattern parity
        return self.color1 if x_pattern == z_pattern else self.color2
