from raytracer.datatypes.color import Color
from raytracer.datatypes.vector import Vector
from raytracer.datatypes.point import Point
from raytracer.datatypes.sphere import Sphere
from raytracer.datatypes.light import PointLight
from raytracer.datatypes.material import Material, ChequerMaterial

WIDTH = 1280
HEIGHT = 1080

RENDERING_IMG = "hd_res.ppm"

CAMERA = Vector(0.0, -0.35, -1.0)

OBJECTS = [
    # Ground plane
    Sphere(
        Point(0, 10000.5, 1),
        10000.0,
        ChequerMaterial(
            color1=Color.from_hex("#420500"),
            color2=Color.from_hex("#e6b87d"),
            ambient=0.2,
            reflection=0.2,
        ),
    ),
    # Blue ball
    Sphere(Point(0.75, -0.1, 1.0), 0.6, Material(Color.from_hex("#0000FF"))),
    Sphere(Point(-0.75, -0.1, 2.25), 0.6, Material(Color.from_hex("#803980"))),
]

LIGHTS = [
    PointLight(Point(1.5, -0.5, -10), Color.from_hex("#FFFFFF")),
    PointLight(Point(-0.5, -10.5, 0), Color.from_hex("#E6E6E6")),
]
