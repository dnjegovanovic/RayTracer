import pytest
from conftest import *

from raytracer.datatypes.image import Image
from raytracer.datatypes.color import Color


def test_image_color():
    w = 3
    h = 2

    im = Image(w, h)
    col_r = Color(r=1.0, g=0.0, b=0.0)
    print(f"color_r: {col_r.r} {col_r.g} {col_r.b}")
    col_g = Color(r=0.0, g=1.0, b=0.0)
    col_b = Color(r=0.0, g=0.0, b=1.0)
    im.set_pixels(0, 0, col_r.data)
    im.set_pixels(1, 0, col_g.data)
    im.set_pixels(2, 0, col_b.data)

    im.set_pixels(0, 1, col_r.data + col_g.data)
    im.set_pixels(1, 1, col_g.data + col_r.data + col_b.data)
    im.set_pixels(2, 1, col_b.data * 0.001)

    with open("test_img.ppm", "w") as img_file:
        im.write_ppm(img_file)
