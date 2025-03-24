import numpy as np


class Image:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = np.zeros((height, width, 3), dtype=np.float32)

    def set_pixels(self, x: int, y: int, color):
        self.pixels[y][x][0] = color.data[0]
        self.pixels[y][x][1] = color.data[1]
        self.pixels[y][x][2] = color.data[2]

    def write_ppm(self, image_file):
        def to_byte(c):
            return round(max(min(c * 255, 255), 0))

        image_file.write(f"P3 {self.width} {self.height}\n255\n")
        for row in self.pixels:
            for col in row:
                image_file.write(
                    f"{to_byte(col[0])} {to_byte(col[1])} {to_byte(col[2])} "
                )
            image_file.write("\n")
