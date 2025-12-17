from typing import Union

import numpy as np
from numpy.typing import NDArray
from PIL import Image


def get_base_img(width: int, height: int) -> Image.Image:
    """Creates an empty black RGB image with the (height, width) size passed."""
    return Image.new("RGB", (width, height), color="black")


def get_base_img_arr(width: int, height: int) -> Image.Image:
    """Creates an empty black RGB image with the (height, width) size passed."""
    return np.zeros((height, width, 3), dtype=np.uint8)


def max_blend_pixel(
    pixel_a: Union[list, tuple], pixel_b: Union[list, tuple]
) -> Union[list, tuple]:
    return pixel_a if sum(pixel_a) > sum(pixel_b) else pixel_b


def max_blend(base: NDArray, top: NDArray, comet_decay: float = 1.0) -> NDArray:
    faded = (base.astype(np.float32) * comet_decay).clip(0, 255).astype(np.uint8)

    return np.maximum(faded, top)
