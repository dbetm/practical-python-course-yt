from typing import Union

import numpy as np
from PIL import Image


def get_base_img(width: int, height: int) -> Image.Image:
    """Creates an empty black RGB image with the (height, width) size passed."""
    return Image.new("RGB", (width, height), color="black")


def get_base_img_arr(width: int, height: int) -> np.array:
    """Creates an empty black image with the (height, width) size"""
    return np.zeros((height, width, 3), dtype=np.uint8)


def max_blend_pixel(pixel_a: Union[list, tuple], pixel_b: Union[list, tuple]):
    return pixel_a if sum(pixel_a) > sum(pixel_b) else pixel_b


def max_blend(base: np.array, top: np.array) -> np.array:
    return np.maximum(base, top)