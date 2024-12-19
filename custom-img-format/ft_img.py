import os
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage

from constants import MAX_INTENSITY, MIN_INTENSITY, CORRUPTED_FILE_MSG_ERR


class FTImage:
    NUM_CHANNELS = 3

    def __init__(self, filepath: str = None, img: PILImage = None):
        if filepath:
            self.img = self.__load(filepath)
        elif img:
            self.img = self.__convert(img)
        else:
            raise Exception("A filepath or a Pillow image must be given")

        self.height = len(self.img)
        self.width = len(self.img[0])

    def __load(self, filepath: str) -> list:
        """Load image saved with format ft from disk. The content is UTF-8 plain text."""
        assert os.path.isfile(filepath), f"The file wasn't found at {filepath}"

        content = list()
        compressed_content = dict()
        max_height = -1
        max_width = -1

        with open(filepath, mode="r") as raw_file:
            lines = raw_file.readlines()

            for line in lines:
                pixel, positions = self.__load_raw_pixel_and_positions(line)

                compressed_content[pixel] = positions

                for (y, x) in positions:
                    if y > max_height:
                        max_height = y
                    if x > max_width:
                        max_width = x

        max_height += 1
        max_width += 1

        content = [[(0, 0, 0) for _ in range(max_width)] for _ in range(max_height)]

        for pixel, positions in compressed_content.items():
            for (y, x) in positions:
                content[y][x] = pixel

        return content

    def __load_raw_pixel_and_positions(self, line: str) -> Tuple[tuple, list]:
        pixel_str, positions_str = line.split(":")

        pixel = tuple(map(int, pixel_str.split(",")))

        assert len(pixel) == self.NUM_CHANNELS, CORRUPTED_FILE_MSG_ERR

        raw_positions = list(map(int, positions_str.split(",")))
        positions = list()

        for idx in range(0, len(raw_positions), 2):
            positions.append(tuple(raw_positions[idx:idx+2]))

        return (pixel, positions)

    def __compress(self) -> dict:
        """Generate the compressed version of the image."""
        compressed_content = dict()

        for y in range(self.height):
            for x in range(self.width):
                pixel = tuple(self.img[y][x])
                if pixel in compressed_content:
                    compressed_content[pixel].append((y, x))
                else:
                    compressed_content[pixel] = [(y, x)]

        return compressed_content

    def __to_raw_string(self, pixel: tuple, positions: list) -> str:
        """Given the pixel and its positions, create a raw string representation."""
        position_to_str = lambda pos : ",".join(map(str, pos)) 
        raw_positions = [position_to_str(pos) for pos in positions]

        return ",".join(map(str, pixel)) + ":" + ",".join(raw_positions)

    def save(self, path: str) -> None:
        """Save image in disk using the FT format."""
        compressed_content = self.__compress()
        num_unique_pixels = len(compressed_content)

        with open(path, "w") as f:
            for idx, (pixel, positions) in enumerate(compressed_content.items()):
                f.write(self.__to_raw_string(pixel, positions))

                if idx < (num_unique_pixels - 1):
                    f.write("\n")

    def change_bright(self, delta: int) -> None:
        """Change bright of all pixels of the image, given a delta change, which could be 
        positive or negative."""
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.img[y][x]
                new_pixel = list()

                for channel_value in pixel:
                    if delta > 0:
                        new_pixel.append(min(MAX_INTENSITY, channel_value + delta))
                    else:
                        new_pixel.append(min(MIN_INTENSITY, channel_value + delta))

                self.img[y][x] = new_pixel

    def to_pil_image(self) -> PILImage:
        np_array = np.array(self.img, dtype=np.uint8)

        return Image.fromarray(np_array, mode="RGB")

    def __str__(self):
        return "\n".join(map(str, self.img))

    def __convert(self, img: PILImage) -> list:
        """Convert Pillow RGB image to ft image."""

        assert img.mode == "RGB", "Error. At this time only RGB images are supported."
        content = list()

        for y in range(img.height):
            row = list()
            for x in range(img.width):
                pixel = list(img.getpixel(xy=(x, y)))
                row.append(pixel)

            content.append(row)

        return content
