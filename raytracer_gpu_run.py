import torch

from raytracer_gpu.datatypes.color import Color
from raytracer_gpu.datatypes.vector import Vector
from raytracer_gpu.datatypes.point import Point
from raytracer_gpu.datatypes.sphere import Sphere
from raytracer_gpu.modules.scene import Scene
from raytracer_gpu.modules.engine import RenderEngine
from raytracer_gpu.datatypes.light import PointLight
from raytracer_gpu.datatypes.material import Material
import importlib
import time

device = "cuda" if torch.cuda.is_available() else "cpu"


def main():
    # WIDTH = 320
    # HEIGHT = 200

    # camera = Vector(torch.tensor([0.0, 0.0, -1.0])).to(device)
    # point = Point(torch.tensor([0, 0, 0])).to(device)
    # color = Color.from_hex("#FF0000", device).to(device)
    # obj = [Sphere(point, 0.5, Material(color))]
    # lights = [
    #     PointLight(
    #         Point(torch.tensor([1.5, -0.5, -10])).to(device),
    #         Color.from_hex("#FFFFFF", device=device).to(device),
    #     )
    # ]

    start_time = time.perf_counter()

    scene_path = "examples.twoballs_gpu"
    mod = importlib.import_module(scene_path)
    
    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engien = RenderEngine(device)
    image = engien.render(scene)

    with open(f"./output/{mod.RENDERING_IMG}", "w") as image_file:
        image.write_ppm(image_file)

    print(f"Total runtime: {time.perf_counter() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
