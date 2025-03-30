from multiprocessing import Process, Value
import multiprocessing as mp
from pathlib import Path
import shutil
import tempfile
import numpy as np
from typing import List, Tuple
import time

from .scene import Scene
from raytracer.datatypes.image import Image
from raytracer.datatypes.ray import Ray
from raytracer.datatypes.point import Point
from raytracer.datatypes.color import Color


class RenderEngine:
    """Renders 3D scenes into 2D images using ray tracing techniques.
    
    Attributes:
        MAX_DEPTH (int): Maximum recursion depth for reflected rays
        MIN_DISPLACE (float): Minimum displacement to prevent self-intersection artifacts
        PROGRESS_UPDATE_INTERVAL (float): Time interval for progress updates in seconds
    """

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001  # Small offset to prevent self-intersection artifacts
    PROGRESS_UPDATE_INTERVAL = 0.5  # Seconds between progress updates

    def render(self, scene: Scene, processes: int = 1) -> Image:
        """Main rendering entry point.
        
        Args:
            scene (Scene): The scene configuration to render
            processes (int): Number of parallel processes to use (default=1)
            
        Returns:
            Image: Rendered image containing pixel color data
        """
        if processes > 1:
            return self._render_multiprocess(scene, processes)
        return self._render_single_process(scene)

    def _render_single_process(self, scene: Scene) -> Image:
        """Renders the scene using a single process.
        
        Suitable for small renders or debugging. Prints progress to stdout.
        """
        width = scene.width
        height = scene.height
        pixels = Image(width, height)

        for j in range(height):
            self._render_row(scene, j, pixels)
            print(f"{j/height*100:3.0f}%", end="\r")

        return pixels

    def _render_multiprocess(self, scene: Scene, process_count: int) -> Image:
        """Renders the scene using multiple parallel processes.
        
        Splits the image into horizontal bands and distributes work across processes.
        Uses shared memory for progress tracking and temporary files for partial results.
        """
        height_ranges = self._split_height_ranges(scene.height, process_count)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            progress = mp.Value("i", 0)  # Shared progress counter
            lock = mp.Lock()  # Progress update lock

            processes = []
            for h_min, h_max in height_ranges:
                p = mp.Process(
                    target=self._render_range,
                    args=(scene, h_min, h_max, temp_dir, progress, lock),
                )
                p.start()
                processes.append(p)

            self._monitor_progress(progress, scene.height)

            for p in processes:
                p.join()

            return self._combine_partials(scene, temp_dir, height_ranges)

    def _render_range(
        self,
        scene: Scene,
        h_min: int,
        h_max: int,
        temp_dir: Path,
        progress: mp.Value,
        lock: mp.Lock,
    ):
        """Renders a vertical slice of the image between h_min and h_max.
        
        Args:
            scene: Scene configuration to render
            h_min: Starting row index (inclusive)
            h_max: Ending row index (exclusive)
            temp_dir: Temporary directory for storing partial results
            progress: Shared counter for tracking completed rows
            lock: Lock for thread-safe progress updates
        """
        try:
            # Create partial image buffer for this range
            partial_img = Image(scene.width, h_max - h_min)

            for j in range(h_min, h_max):
                y = j - h_min
                self._render_row(scene, j, partial_img, y_offset=y)

                # Update progress counter with thread-safe lock
                with lock:
                    progress.value += 1

            # Save partial results to numpy array
            np.save(temp_dir / f"partial_{h_min}.npy", partial_img.pixels)

        except Exception as e:
            print(f"\nError rendering {h_min}-{h_max}: {str(e)}")
            raise

    def _calculate_y(self, row_idx: int, aspect_ratio: float, height: int) -> float:
        """Calculates vertical screen space coordinate for a given row.
        
        Converts pixel row index to normalized device coordinates.
        """
        y0 = -1.0 / aspect_ratio  # Bottom of screen
        y1 = 1.0 / aspect_ratio   # Top of screen
        return y0 + row_idx * (y1 - y0) / (height - 1)  # Linear interpolation

    @staticmethod
    def _split_height_ranges(total_height: int, parts: int) -> List[Tuple[int, int]]:
        """Divides image height into approximately equal ranges for parallel processing.
        
        Example: For 100px height and 3 processes → [(0,34), (34,67), (67,100)]
        """
        base, rem = divmod(total_height, parts)
        return [
            (i * base + min(i, rem), (i + 1) * base + min(i + 1, rem))
            for i in range(parts)
        ]

    def _render_row(self, scene: Scene, row_idx: int, image: Image, y_offset: int = 0):
        """Renders a single row of pixels.
        
        Core ray tracing logic for generating pixel colors.
        """
        width = scene.width
        aspect_ratio = float(width) / scene.height
        x0, x1 = -1.0, 1.0  # Screen space X boundaries
        x_step = (x1 - x0) / (width - 1)
        y = self._calculate_y(row_idx, aspect_ratio, scene.height)

        for i in range(width):
            # Calculate screen space X coordinate
            x = x0 + i * x_step
            # Create ray from camera through current pixel
            direction = Point(x, y) - scene.camera
            ray = Ray(scene.camera, direction)
            # Trace ray and store resulting color
            color = self.ray_trace(ray, scene)
            image.set_pixels(i, y_offset, color)

    def _combine_partials(
        self, scene: Scene, temp_dir: Path, ranges: List[Tuple[int, int]]
    ) -> Image:
        """Combines partial renders from temporary files into final image."""
        final_image = Image(scene.width, scene.height)

        for h_min, h_max in ranges:
            partial_path = temp_dir / f"partial_{h_min}.npy"
            partial_pixels = np.load(partial_path)
            final_image.pixels[h_min:h_max] = partial_pixels

        return final_image

    def _monitor_progress(self, progress: mp.Value, total: int):
        """Displays and updates rendering progress in the console."""
        start_time = time.time()
        last_print = 0  # Last progress update time

        while True:
            time.sleep(0.1)
            current = progress.value
            elapsed = time.time() - start_time

            if current >= total:
                print(f"\nRendering complete in {elapsed:.1f}s")
                return

            # Throttle progress updates to specified interval
            if time.time() - last_print > self.PROGRESS_UPDATE_INTERVAL:
                percent = current / total * 100
                remaining = (
                    (elapsed / current) * (total - current) if current > 0 else 0
                )
                print(
                    f"{percent:5.1f}% | Elapsed: {elapsed:5.1f}s | Remaining: {remaining:5.1f}s",
                    end="\r",
                )
                last_print = time.time()

    def ray_trace(self, ray, scene, depth=0):
        """Traces a ray through the scene with recursion for reflections.
        
        Args:
            ray: Ray to trace
            scene: Scene configuration
            depth: Current recursion depth (for reflections)
            
        Returns:
            Color: Accumulated color at this ray intersection
        """
        color = Color(0.0, 0.0, 0.0)
        # Find nearest object intersected by ray
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color  # No intersection → return background color

        # Calculate hit position and surface normal
        hit_pos = ray.org + ray.dir * dist_hit
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, scene, hit_normal)

        # Handle reflections recursively
        if depth < self.MAX_DEPTH:
            # Offset new ray origin to prevent self-intersection
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            # Calculate reflection direction
            new_ray_dir = (
                ray.dir - 2 * ray.dir.dot_product(hit_normal.data) * hit_normal
            )
            new_ray = Ray(new_ray_pos, new_ray_dir)
            # Add reflected color attenuated by material's reflection coefficient
            color += (
                self.ray_trace(new_ray, scene, depth=depth + 1)
                * obj_hit.material.reflection
            )

        return color

    def find_nearest(self, ray, scene):
        """Finds the closest object intersecting with the ray.
        
        Returns:
            Tuple[float, Object]: Distance to nearest object and the object itself
        """
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

    def color_at(self, obj_hit, hit_pos, scene, hit_normal):
        """Calculates surface color at hit position considering lighting.
        
        Combines:
        - Ambient lighting
        - Diffuse shading (Lambertian reflectance)
        - Specular highlights (Blinn-Phong model)
        """
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_camera = scene.camera - hit_pos  # Vector to camera position
        specular_k = 50  # Specular exponent for highlight tightness

        # Start with ambient component
        color = material.ambient * Color.from_hex("#000000")

        # Calculate lighting contribution from all light sources
        for light in scene.lights:
            to_light = Ray(hit_pos, (light.positions - hit_pos))

            # Diffuse component (Lambertian reflectance)
            diffuse_strength = max(hit_normal.dot_product(to_light.dir.data), 0)
            color += (
                obj_color
                * material.diffuse
                * diffuse_strength
            )

            # Specular component (Blinn-Phong)
            half_vec = (to_light.dir + to_camera).normalize
            specular_strength = max(hit_normal.dot_product(half_vec.data), 0)
            color += (
                light.color
                * material.specular
                * (specular_strength ** specular_k)
            )

        return color