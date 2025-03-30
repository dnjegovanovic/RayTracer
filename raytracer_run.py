import argparse
import importlib
from multiprocessing import cpu_count

from raytracer.modules.scene import Scene
from raytracer.modules.engine_mp import RenderEngine

import importlib
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scene",default="examples.twoballs", help="Path to scene file (without .py extension)")
    args = parser.parse_args()
    
    start_time = time.perf_counter()

    mod = importlib.import_module(args.scene)

    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engien = RenderEngine()
    image = engien.render(scene)

    with open(f"./output/{mod.RENDERING_IMG}", "w") as image_file:
        image.write_ppm(image_file)

    print(f"Total runtime: {time.perf_counter() - start_time:.2f} seconds")

def mp_main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scene",
        default="examples.twoballs",
        help="Path to scene file (without .py extension)",
    )
    parser.add_argument(
        "-p",
        "--processes",
        action="store",
        type=int,
        dest="processes",
        default=0,
        help="Number of processes (0=auto)",
    )
    args = parser.parse_args()
    if args.processes == 0:
        process_count = cpu_count()
    else:
        process_count = args.processes

    start_time = time.perf_counter()

    mod = importlib.import_module(args.scene)

    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine()
    # Multiprocess (4 workers)
    image = engine.render(scene, processes=process_count)

    with open(f"./output/{mod.RENDERING_IMG}", "w") as image_file:
        image.write_ppm(image_file)


if __name__ == "__main__":
    mp_main()
