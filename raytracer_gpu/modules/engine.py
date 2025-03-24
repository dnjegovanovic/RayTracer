import torch

from .scene import Scene
from raytracer_gpu.datatypes.image import Image
from raytracer_gpu.datatypes.ray import Ray
from raytracer_gpu.datatypes.point import Point
from raytracer_gpu.datatypes.color import Color


class RenderEngine:
    """Render 3D objs into 2D using raytracing"""

    def __init__(self, device="cpu"):
        self.device = device

    def render(self, scene: Scene):
        width = scene.width
        height = scene.height
        aspect_ration = float(width) / height

        x0 = -1.0
        x1 = 1.0
        x_step = (x1 - x0) / (width - 1)

        y0 = -1.0 / aspect_ration
        y1 = 1.0 / aspect_ration
        y_step = (y1 - y0) / (height - 1)

        camera = scene.camera
        pixels = Image(width, height, device=self.device)
        for j in range(height):
            y = y0 + j * y_step
            for i in range(width):
                x = x0 + i * x_step
                dir = Point(torch.tensor([x, y])).to(self.device) - camera
                ray = Ray(camera, dir)
                pixels.set_pixels(i, j, self.ray_trace(ray, scene))

        return pixels

    def ray_trace(self, ray, scene):
        color = Color(torch.tensor([0.0, 0.0, 0.0])).to(self.device)
        # Finde the nearest obj hit by ray in the scene
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color.get_color

        hit_pos = ray.org + ray.dir * dist_hit
        hit_color = self.color_at(obj_hit, hit_pos, scene)
        color += hit_color

        return color.get_color

    def find_nearest(self, ray, scene):
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

    def color_at(self, obj_hit, hit_pos, scene):
        return obj_hit.material
