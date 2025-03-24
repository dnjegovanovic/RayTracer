from .scene import Scene
from raytracer.datatypes.image import Image
from raytracer.datatypes.ray import Ray
from raytracer.datatypes.point import Point
from raytracer.datatypes.color import Color


class RenderEngine:
    """Render 3D objs into 2D using raytracing"""

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
        pixels = Image(width, height)
        for j in range(height):
            y = y0 + j * y_step
            for i in range(width):
                x = x0 + i * x_step
                dir = Point(x, y) - camera
                ray = Ray(camera, dir)
                pixels.set_pixels(i, j, self.ray_trace(ray, scene))

        return pixels

    def ray_trace(self, ray, scene):
        color = Color(0.0, 0.0, 0.0)
        # Finde the nearest obj hit by ray in the scene
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color

        hit_pos = ray.org + ray.dir * dist_hit
        color += self.color_at(obj_hit, hit_pos, scene)

        return color

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
