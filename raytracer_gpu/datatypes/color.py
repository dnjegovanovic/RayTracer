import torch
from tensordict import tensorclass
from .vector import Vector


@tensorclass
class Color(Vector):
    """RGB color representation with value clamping (0-1 range).
    
    Inherits from Vector but adds:
    - RGB component aliases (r, g, b)
    - Automatic value clamping
    - Color-specific operations
    
    Example:
        >>> c = Color(r=1.5, g=0.5, b=-0.2)
        >>> c.r  # 1.0 (clamped)
        >>> c.g  # 0.5
        >>> c.b  # 0.0
    """
    
    def __post_init__(self):
        # First validate vector shape via parent
        super().__post_init__()
        # Then clamp values to 0-1 range
        self._vector = torch.clamp(self._vector, 0.0, 1.0)
    
    
    @classmethod
    def from_rgb(cls, r: float, g: float, b: float) -> "Color":
        """Create Color from RGB values"""
        return cls(_vector=torch.tensor([r, g, b], dtype=torch.float32))
    
    @classmethod
    def from_vector(cls, vector: Vector) -> "Color":
        """Create Color from existing Vector"""
        return cls(_vector=vector._vector)

    @property
    def r(self) -> float:
        return self.x

    @property
    def g(self) -> float:
        return self.y

    @property
    def b(self) -> float:
        return self.z
    
    @property
    def get_color(self) -> torch.Tensor:
        return self._vector

    # Override operators to return Color instances
    def __add__(self, other: Vector) -> "Color":
        result = super().__add__(other)
        return Color(_vector=result._vector)

    def __sub__(self, other: Vector) -> "Color":
        result = super().__sub__(other)
        return Color(_vector=result._vector)

    def __mul__(self, scalar) -> "Color":
        result = super().__mul__(scalar)
        return Color(_vector=result._vector)

    def __rmul__(self, scalar) -> "Color":
        return self.__mul__(scalar)

    def __truediv__(self, scalar) -> "Color":
        result = super().__truediv__(scalar)
        return Color(_vector=result._vector)

    def mix(self, other: "Color", ratio: float) -> "Color":
        """Linear color interpolation"""
        return Color(_vector=self._vector * ratio + other._vector * (1 - ratio))