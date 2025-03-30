from raytracer_gpu.datatypes.color import Color
from raytracer_gpu.datatypes.vector import Vector
from raytracer_gpu.datatypes.point import Point
from raytracer_gpu.datatypes.sphere import Sphere
from raytracer_gpu.datatypes.light import PointLight
from raytracer_gpu.datatypes.material import Material, ChequerMaterial
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

WIDTH = 960
HEIGHT = 540

RENDERING_IMG = "2balls_cpu_refl_res2_gpu.ppm"

CAMERA = Vector(torch.tensor([0.0, -0.35, -1.0])).to(device)

OBJECTS = [
    # Ground plane
    Sphere(
        Point(torch.tensor([0, 10000.5, 1])).to(device),
        10000.0,
        ChequerMaterial(
            color1=Color.from_hex("#420500").to(device),
            color2=Color.from_hex("#e6b87d").to(device),
            ambient=0.2,
            reflection=0.2,
        ),
    ),
    # Blue ball
    Sphere(
        Point(torch.tensor([0.75, -0.1, 1.0])).to(device),
        0.6,
        Material(Color.from_hex("#0000FF", device).to(device)),
    ),
    Sphere(
        Point(torch.tensor([-0.75, -0.1, 2.25])).to(device),
        0.6,
        Material(Color.from_hex("#803980", device).to(device)),
    ),
]

LIGHTS = [
    PointLight(
        Point(torch.tensor([1.5, -0.5, -10])).to(device),
        Color.from_hex("#FFFFFF", device).to(device),
    ),
    PointLight(
        Point(torch.tensor([-0.5, -10.5, 0])).to(device),
        Color.from_hex("#E6E6E6", device).to(device),
    ),
]
