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

            print("{:3.0f}%".format(float(j) / float(height) * 100), end="\r")

        return pixels

    def ray_trace(self, ray, scene):
        color = Color(0.0, 0.0, 0.0)
        # Finde the nearest obj hit by ray in the scene
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color

        hit_pos = ray.org + ray.dir * dist_hit
        # Calc normal at hit poissition
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, scene, hit_normal)

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

    def color_at(self, obj_hit, hit_pos, scene, hit_normal):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_camera = scene.camera - hit_pos
        specular_k = 50
        color = material.ambient * Color.from_hex("#000000")
        # Calculate for all lights in the scene
        for light in scene.lights:
            to_light = Ray(hit_pos, (light.positions - hit_pos))
            # Diffusion shading (Lambert)
            color += (
                obj_color
                * material.diffuse
                * max(hit_normal.dot_product(to_light.dir.data), 0)
            )

            # Specular shading (Blinn-Phone)
            half_vec = (to_light.dir + to_camera).normalize
            color += (
                light.color
                * material.specular
                * max(hit_normal.dot_product(half_vec.data), 0) ** specular_k
            )
        return color
