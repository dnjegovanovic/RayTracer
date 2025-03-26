from raytracer.datatypes.color import Color
from raytracer.datatypes.vector import Vector
from raytracer.datatypes.point import Point
from raytracer.datatypes.sphere import Sphere
from raytracer.modules.scene import Scene
from raytracer.modules.engine import RenderEngine
from raytracer.datatypes.light import PointLight
from raytracer.datatypes.material import Material


def main():
    WIDTH = 320
    HEIGHT = 200

    camera = Vector(0.0, 0.0, -1.0)
    obj = [Sphere(Point(0, 0, 0), 0.5, Material(Color.from_hex("#FF0000")))]
    lights = [PointLight(Point(1.5, -0.5, -10), Color.from_hex("#FFFFFF"))]

    scene = Scene(camera, obj, lights, WIDTH, HEIGHT)
    engien = RenderEngine()
    image = engien.render(scene)

    with open("./output/test_shading.ppm", "w") as image_file:
        image.write_ppm(image_file)


if __name__ == "__main__":
    main()
