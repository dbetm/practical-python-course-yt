from typing import Union
from PIL import Image


def get_base_img(width: int, height: int) -> Image.Image:
    """Creates an empty black RGB image with the (height, width) size passed."""
    return Image.new("RGB", (width, height), color="black")


def max_blend_pixel(pixel_a: Union[list, tuple], pixel_b: Union[list, tuple]):
    return pixel_a if sum(pixel_a) > sum(pixel_b) else pixel_b