import os

import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage

from constants import MAX_INTENSITY, MIN_INTENSITY


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
        """Load image saved with format ft from disk. The content is plain text."""
        assert os.path.isfile(filepath), f"The file wasn't found at {filepath}"

        content = list()

        with open(filepath, mode="r") as raw_file:
            lines = raw_file.readlines()

            for line in lines:
                raw_row = line.split(",")
                raw_row[-1] = raw_row[-1].replace("\n", "")
                raw_row = list(map(int, raw_row))

                assert len(raw_row) % self.NUM_CHANNELS == 0, "Error trying to read image, corrupted file."

                row = list()
                for idx in range(0, len(raw_row), self.NUM_CHANNELS):
                    row.append(raw_row[idx:idx+self.NUM_CHANNELS])

                content.append(row)

        return content

    def save(self, path: str) -> None:
        """Save image in disk using the FT format."""
        row_to_raw = lambda row : ",".join([",".join(map(str, pixel)) for pixel in row])

        with open(path, "w") as f:
            for idx, row in enumerate(self.img):
                f.write(row_to_raw(row))

                if idx < (len(self.img) - 1):
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
