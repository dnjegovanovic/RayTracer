from raytracer.datatypes.color import Color
from raytracer.datatypes.vector import Vector
from raytracer.datatypes.point import Point
from raytracer.datatypes.sphere import Sphere
from raytracer.modules.scene import Scene
from raytracer.modules.engine import RenderEngine
from raytracer.datatypes.light import PointLight
from raytracer.datatypes.material import Material

import importlib
import time

def main():
    start_time = time.perf_counter()

    scene_path = "examples.twoballs"
    mod = importlib.import_module(scene_path)

    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engien = RenderEngine()
    image = engien.render(scene)

    with open(f"./output/{mod.RENDERING_IMG}", "w") as image_file:
        image.write_ppm(image_file)

    print(f"Total runtime: {time.perf_counter() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
