import os
from typing import List

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
        """Load image saved with format ft from disk. The content is plain text."""
        assert os.path.isfile(filepath), f"The file wasn't found at {filepath}"

        content = list()

        with open(filepath, mode="r") as raw_file:
            lines = raw_file.readlines()

            for line in lines:
                raw_row = self.__uncompress(line)

                assert len(raw_row) % self.NUM_CHANNELS == 0, CORRUPTED_FILE_MSG_ERR

                row = list()
                for idx in range(0, len(raw_row), self.NUM_CHANNELS):
                    row.append(raw_row[idx:idx+self.NUM_CHANNELS])

                content.append(row)

        return content


    def __uncompress(self, raw_row_str: str) -> List[int]:
        """Uncompress raw string line expanding numbers by the associated factor if applied."""
        row_uncompressed = list()
        number_str = list()
        factor_str = list()
        idx = 0
        n = len(raw_row_str)

        print(raw_row_str)

        while idx < n:
            char = raw_row_str[idx]

            if char >= "0" and char <= "9":
                number_str.append(char)

                if idx == (n-2) and raw_row_str[idx+1] == "\n" or idx == (n-1):
                    num = int("".join(number_str))
                    row_uncompressed.append(num)

                    number_str = list()
            elif char == ",":
                num = int("".join(number_str))
                row_uncompressed.append(num)

                number_str = list()
            elif char == "[":
                idx += 1
                while raw_row_str[idx] != "]" and idx < n:
                    factor_str.append(raw_row_str[idx])
                    idx += 1

                num = int("".join(number_str))
                factor = int("".join(factor_str))

                row_uncompressed += [num]*factor

                number_str = list()
                factor_str = list()
            elif char == "\n": # to discard breakline
                pass
            else:
                print(f"char not supported: {char}")
                raise Exception(CORRUPTED_FILE_MSG_ERR)

            idx += 1

        print(row_uncompressed)
        return row_uncompressed

    def __compress(self, row: list) -> str:
        """Given a row with the pixels, generate the compressed version of the raw row."""
        flat_row = [ch_val for pixel in row for ch_val in pixel]
        compressed_row = list()

        n = len(flat_row)
        reference_value = flat_row[0]
        factor = 1
        idx = 1

        while idx < n:
            if flat_row[idx] == reference_value:
                factor += 1
            elif factor > 1:
                compressed_row.append(f"{reference_value}[{factor}]")
                reference_value = flat_row[idx]
                factor = 1
            else:
                compressed_row.append(str(reference_value))
                reference_value = flat_row[idx]
                factor = 1

                if idx < (n-1):
                    compressed_row.append(",")

            idx += 1

        # consider the last value(s)
        if factor > 1:
            compressed_row.append(f"{reference_value}[{factor}]")
        else:
            compressed_row.append(f",{reference_value}")

        return "".join(compressed_row)

    def save(self, path: str) -> None:
        """Save image in disk using the FT format."""
        with open(path, "w") as f:
            for idx, row in enumerate(self.img):
                f.write(self.__compress(row))

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