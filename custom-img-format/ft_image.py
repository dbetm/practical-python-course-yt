import os

import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage


class FTImage:
    NUM_CHANNELS = 3
    MODE = "RGB"

    def __init__(self, filepath: str = None, img: PILImage = None):
        if filepath:
            self.img = self.__load(filepath) # self.img is a list of lists (matrix)
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

        with open(filepath, mode="r") as file:
            lines = file.readlines()
        
        for line in lines:
            raw_row = line.split(",")
            raw_row[-1] = raw_row[-1].replace("\n", "")
            raw_row = list(map(int, raw_row))

            assert len(raw_row) % self.NUM_CHANNELS == 0, "Error trying to read image, corrupted file"

            row = list()
            for idx in range(0, len(raw_row), self.NUM_CHANNELS):
                row.append(raw_row[idx:idx+self.NUM_CHANNELS])
            
            content.append(row)

        return content

    def __convert(self, img: PILImage) -> list:
        """Convert Pillow RGB image to ft image."""
        content = list()

        assert img.mode == self.MODE, "Error. Only RGB images are supported."

        for y in range(img.height):
            row = list()
            for x in range(img.width):
                pixel = list(img.getpixel(xy=(x, y)))
                row.append(pixel)

            content.append(row)

        return content

    def save(self, path: str) -> None:
        """Save image in disk using the FT format."""

        row_to_raw = lambda row : ",".join([",".join(map(str, pixel)) for pixel in row])

        with open(path, "w") as f:
            for idx, row in enumerate(self.img):
                f.write(row_to_raw(row))

                if idx < (self.height - 1):
                    f.write("\n")

    def to_pil_image(self) -> PILImage:
        np_array = np.array(self.img, dtype=np.uint8)
        return Image.fromarray(np_array, mode=self.MODE)

    def __str__(self):
        return "\n".join(map(str, self.img))