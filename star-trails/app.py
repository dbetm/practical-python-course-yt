import logging
import os
import sys
from typing import List, Tuple

import numpy as np
from PIL import Image
from tqdm import tqdm

from images import get_base_img, get_base_img_arr, max_blend, max_blend_pixel
from timelapse import Timelapse

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(name="app")


class StarTrail:
    def __init__(self, images_path: str):
        self.images_path = images_path
        # load filenames
        self.filenames = self.__load_filenames()
        # sort filenames
        self.filenames.sort()
        # get image dimensions and check that each image has that size
        self.img_height, self.img_width = self.__get_dims()

        self.__check_dims()

    def __load_filenames(self) -> List[str]:
        return [
            filename
            for filename in os.listdir(images_path)
            if not filename.startswith(".")
        ]

    def __get_dims(self) -> Tuple[int, int]:
        with Image.open(os.path.join(self.images_path, self.filenames[0])) as img:
            return img.height, img.width

    def __check_dims(self) -> None:
        logger.info("Checking size for each image...")

        for filename in tqdm(self.filenames):
            img_filepath = os.path.join(self.images_path, filename)

            with Image.open(img_filepath) as img:
                if img.width != self.img_width or img.height != self.img_height:
                    raise ValueError("All images must have the same size!")

        logger.info("Great! All images have the same size")

    def generate(self, img_output_filepath: str, blend_fn: callable) -> None:
        star_trails_img = get_base_img(self.img_width, self.img_height)

        logger.info("Generating star trails image...blending")
        for filename in tqdm(self.filenames):
            img_filepath = os.path.join(self.images_path, filename)

            with Image.open(img_filepath) as img:
                for y in range(img.height):
                    for x in range(img.width):
                        base_pixel = star_trails_img.getpixel((x, y))
                        top_pixel = img.getpixel((x, y))

                        new_pixel = blend_fn(base_pixel, top_pixel)

                        star_trails_img.putpixel(xy=(x, y), value=new_pixel)

        star_trails_img.save(img_output_filepath)

    def generate_opt(
        self, frames_path: str, blend_fn: callable, addition_kargs_blend: dict = {}
    ) -> None:
        star_trails = get_base_img_arr(self.img_width, self.img_height)

        os.makedirs(frames_path, exist_ok=True)

        logger.info("Generating star trails image...blending")
        for idx, filename in enumerate(tqdm(self.filenames)):
            img_filepath = os.path.join(self.images_path, filename)

            img = np.array(Image.open(img_filepath), dtype=np.uint8)

            star_trails = blend_fn(star_trails, img, **addition_kargs_blend)

            star_trails_img = Image.fromarray(star_trails)
            star_trails_img.save(
                os.path.join(frames_path, f"{idx+1}_frame.jpg"), format="JPEG"
            )


if __name__ == "__main__":
    images_path = (
        "/Volumes/Extreme SSD/astro/noches-estrelladas/2025/2025-agosto-19/"
        "fotos-estrellas-para-star-trails-19-agosto-2025"
    )
    output_path = os.path.join("output", "frames")

    session = StarTrail(images_path)

    session.generate_opt(
        output_path,
        max_blend,
        addition_kargs_blend={"comet_decay": 0.999999},
    )

    timelapser = Timelapse(output_path, fps=30)

    output_timelapse_path = os.path.join(
        "output", "timelapses", "star_trails_timelapse.mp4"
    )

    timelapser.make(output_timelapse_path)
