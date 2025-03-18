import torch

from conftest import *
import pytest

from raytracer_gpu.datatypes.vector import Vector

DEVICE = torch.device("cuda:0")


def test_vector_operation():
    v_t1 = torch.Tensor([1.0, -2.0, -2.0])
    v_t2 = torch.Tensor([1.0, 1.0, 1.0])
    v1 = Vector(v_t1).to(DEVICE)
    v1.requires_grad_(True)
    assert v1.mag == 3.0, "Magnitude of vector should be 3!"

    v2 = Vector(v_t2).to(DEVICE)
    v2.requires_grad_(True)
    dot_p = v1.dot_product(v2)
    assert dot_p == -3.0, "V1 must be same as dot_p!"

    add_o = v1 + v2
    assert add_o.x == 2.0, "x must be wrong!"

    mul_o = v2 * 2.0
    assert mul_o.x == 2.0, "res should be 2.0!"

    div_o = v2 / 1.0
    assert div_o.x == 1.0, "res should be 2.0!"
