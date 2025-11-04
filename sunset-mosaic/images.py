import os
import random
from typing import Optional, Tuple

import pandas as pd
from tqdm import tqdm
from PIL import Image

from utils import compute_euclidian_distance


def redim_image_dataset(
    dim: int, input_dataset_path: str, output_dataset_path: str
) -> None:
    files = os.listdir(input_dataset_path)

    os.makedirs(output_dataset_path, exist_ok=True)
    format_img_filename = lambda filename : f"{filename.split('.')[0]}.png"

    for file in tqdm(files):
        if file == ".DS_Store":
            continue
        with Image.open(os.path.join(input_dataset_path, file)) as img:
            img.thumbnail((dim, dim), Image.Resampling.LANCZOS)
            img.save(
                os.path.join(output_dataset_path, format_img_filename(file)),
                format="PNG"
            )


def get_average_per_channel(img: Image, n: Optional[int] = None) -> Tuple[float, float, float]:
    r_sum, g_sum, b_sum = 0, 0, 0

    if n:
        sample_size = min(n, img.width * img.height)
        margin = 5

        for _ in range(sample_size):
            x = random.randint(0, img.width - margin)
            y = random.randint(0, img.height - margin)
            pixel = img.getpixel((x, y))

            r_sum += pixel[0]
            g_sum += pixel[1]
            b_sum += pixel[2]

        return (r_sum / sample_size, g_sum / sample_size, b_sum / sample_size)

    total_pixels = img.width * img.height

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))

            r_sum += pixel[0]
            g_sum += pixel[1]
            b_sum += pixel[2]

    return (r_sum / total_pixels, g_sum / total_pixels, b_sum / total_pixels)



def compute_nearest_images(
    metadata: pd.DataFrame, avg_per_channel: tuple, k: int = 3
) -> list:
    distances_serie = metadata.apply(
        lambda row: (
            compute_euclidian_distance(
                a=list(avg_per_channel),
                b=[row["r_avg"], row["g_avg"], row["b_avg"]]
            ),
            row["file"],
        ),
        axis=1
    )

    distances_files = list(distances_serie)
    distances_files.sort()

    return [filename for dis, filename in distances_files[:k]]



def resize_img(img: Image.Image, max_size: int) -> Image:
    """Resize a PIL Image so its longest side is exactly max_size, preserving aspect ratio.
    This will upscale images smaller than max_size and downscale images larger than max_size.
    """
    width, height = img.size
    # Compute scaling factor so that the longest side becomes max_size
    scale = max_size / float(max(width, height))
    new_size = (int(round(width * scale)), int(round(height * scale)))

    # Use high-quality resampling filter
    return img.resize(new_size, Image.Resampling.LANCZOS)