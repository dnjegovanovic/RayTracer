import numpy as np

from conftest import *
import pytest

from raytracer.datatypes.vector import Vector


def test_vector_operation():
    v1 = Vector(1.0, -2.0, -2.0)
    assert v1.mag == 3.0, "Magnitude of vector should be 3!"

    v2 = Vector(1.0, 1.0, 1.0)
    dot_p = v1.dot_product(v2.data)
    assert dot_p == -3.0, "V1 must be same as dot_p!"

    add_o = v1 + v2
    assert add_o.x == 2.0, "x must be wrong!"

    mul_o = v2 * 2.0
    assert mul_o.x == 2.0, "res should be 2.0!"

    div_o = v2 / 1.0
    assert div_o.x == 1.0, "res should be 2.0!"
