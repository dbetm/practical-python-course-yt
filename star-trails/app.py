import os
import logging
import sys
from typing import List, Tuple

from PIL import Image
from tqdm import tqdm

from images import get_base_img, max_blend_pixel


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(name="app")


class StarTrail:
    def __init__(self, images_path: str):
        self.images_path = images_path
        self.filenames = self.__load_filenames()
        self.filenames.sort() # keep ordered
        self.img_height, self.img_width = self.__get_dims()

        self.__check_dims()

    def __load_filenames(self) -> List[str]:
        return [filename for filename in os.listdir(images_path) if not filename.startswith(".")]

    def __get_dims(self) -> Tuple[int, int]:
        with Image.open(os.path.join(self.images_path, self.filenames[0])) as img:
            return img.height, img.width

    def __check_dims(self):
        logger.info("Checking size for each image...")

        for filename in tqdm(self.filenames):
            img_filepath = os.path.join(self.images_path, filename)
            with Image.open(img_filepath) as img:
                if img.width != self.img_width or img.height != self.img_height:
                    raise ValueError("All images must have the same size")

        logger.info("Great! All images has the same size")

    def generate(self, img_output_filepath: str, blend_method: callable) -> None:
        star_trails_img = get_base_img(self.img_width, self.img_height)

        logger.info("Generating star trails image...blending")
        for filename in tqdm(self.filenames):
            img_filepath = os.path.join(images_path, filename)

            with Image.open(img_filepath) as img:

                for y in range(img.height):
                    for x in range(img.width):
                        base_pixel = star_trails_img.getpixel((x, y))
                        top_pixel = img.getpixel((x, y))

                        new_pixel = blend_method(base_pixel, top_pixel)

                        star_trails_img.putpixel(xy=(x, y), value=new_pixel)

        star_trails_img.save(img_output_filepath)


if __name__ == "__main__":
    images_path = (
        "/Volumes/Extreme SSD/astro/noches-estrelladas/2025/2025-agosto-19/"
        "fotos-estrellas-para-star-trails-19-agosto-2025"
    )

    session = StarTrail(images_path)

    session.generate(os.path.join("images", "result1.png"), blend_method=max_blend_pixel)