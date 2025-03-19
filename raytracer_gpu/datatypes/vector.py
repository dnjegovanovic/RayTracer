import torch
from tensordict import tensorclass


@tensorclass
class Vector:
    """A 3D vector implementation for geometric operations, backed by PyTorch tensors.

    Features:
    - Tensor storage (shape [..., 3]) with batch support via `tensordict`
    - Common vector operations: magnitude, normalization, dot product
    - Operator overloads (+/- for vector math, * for scalar multiplication)
    - GPU/CPU compatible and autograd-friendly

    Attributes:
        vector: 3D Tesor: (x,y,z)

    Example:
        >>> v = Vector(torch.tensor([1.0, 2.0, 3.0]))
        >>> v.x  # 1.0 (float)
        >>> v.vector  # tensor([1., 2., 3.])
        >>> v.normalize.mag  # tensor(1.0)
    """

    _vector: torch.Tensor  # Tensor field for 3D vector

    def __post_init__(self):
        assert self._vector.shape[-1] == 3, "Vector must have 3 elements"

    @property
    def x(self) -> float:
        return self._vector[0].item()

    @property
    def y(self) -> float:
        return self._vector[1].item()

    @property
    def z(self) -> float:
        return self._vector[2].item()

    @property
    def mag(self) -> torch.Tensor:
        return torch.norm(self._vector)

    @property
    def normalize(self) -> "Vector":
        return Vector(self._vector / self.mag)

    def dot_product(self, other: "Vector") -> torch.Tensor:
        return torch.dot(self._vector, other._vector)

    def __mul__(self, scalar) -> "Vector":
        if isinstance(scalar, (int, float)):
            return Vector(self._vector * scalar)
        else:
            raise TypeError(
                f"Unsupported operand type for *: Vector and {type(scalar)}"
            )

    def __rmul__(self, scalar) -> "Vector":
        return self.__mul__(scalar)

    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self._vector + other._vector)
        else:
            raise TypeError(f"Unsupported operand type for +: Vector and {type(other)}")

    def __sub__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self._vector - other._vector)
        else:
            raise TypeError(f"Unsupported operand type for -: Vector and {type(other)}")

    def to(self, device):
        self._vector = self._vector.to(device)
        return self

    def detach(self):
        """Detach from autograd cmoputation

        Returns:
            _vector: the detached _vector.
        """
        self._vector = self._vector.detach()
        return self

    def requires_grad_(self, val: bool):
        """Enable or disable gradient computation for internal parameters

        Calling this wiht val=True will make the internal properties a leaf node
        in the autograd graph, which enables optimization with the standard
        PyTorch facilities.

        Args:
            val (bool): enable or disable gradient computation
        """
        self._vector.requires_grad_(val)
