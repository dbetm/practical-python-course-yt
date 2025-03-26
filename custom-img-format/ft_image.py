import os
from abc import ABC, abstractmethod
from typing import List

import numpy as np
from PIL import Image
from PIL.Image import Image as PILImage


class RGBFormat(ABC):
    NUM_CHANNELS = 3
    MODE = "RGB"

    def __init__(self, filepath: str = None, img: PILImage = None):
        if filepath:
            self.img = self._load(filepath) # self.img is a list of lists (matrix)
        elif img:
            self.img = self._convert(img)
        else:
            raise Exception("A filepath or a Pillow image must be given")

        self.height = len(self.img)
        self.width = len(self.img[0])

    def to_pil_image(self) -> PILImage:
        np_array = np.array(self.img, dtype=np.uint8)
        return Image.fromarray(np_array, mode=self.MODE)

    def __str__(self):
        return "\n".join(map(str, self.img))

    def _convert(self, img: PILImage) -> list:
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

    @abstractmethod
    def _load(self, filepath: str) -> list:
        """Load image saved with format ft from disk. The content is plain text."""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Save image in disk using the FT format."""
        pass


class FTImage(RGBFormat):
    def _load(self, filepath: str) -> list:
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

    def save(self, path: str) -> None:
        """Save image in disk using the FT format."""

        row_to_raw = lambda row : ",".join([",".join(map(str, pixel)) for pixel in row])

        with open(path, "w") as f:
            for idx, row in enumerate(self.img):
                f.write(row_to_raw(row))

                if idx < (self.height - 1):
                    f.write("\n")


class FTImage2(RGBFormat):
    def _load(self, filepath: str) -> list:
        """Load image saved with format ft from disk. The content is plain text."""
        assert os.path.isfile(filepath), f"The file wasn't found at {filepath}"

        content = list()

        with open(filepath, mode="r") as file:
            lines = file.readlines()

        for line in lines:
            raw_row = self.__uncompress(line)

            assert len(raw_row) % self.NUM_CHANNELS == 0, "Error trying to read image, corrupted file"

            row = list()
            for idx in range(0, len(raw_row), self.NUM_CHANNELS):
                row.append(raw_row[idx:idx+self.NUM_CHANNELS])
            
            content.append(row)

        return content

    def save(self, path: str) -> None:
        """Save image in disk using the FT format."""
        with open(path, "w") as f:
            for idx, row in enumerate(self.img):
                f.write(self.__compress(row))

                if idx < (self.height - 1):
                    f.write("\n")

    def __uncompress(self, raw_row: str) -> List[int]:
        """Uncompress raw string line expanding numbers by the associated factor if applied.

        "0[3]255[3]255,0,255,0,255,0\n" === expected ====> [0, 0, 0, 255, 255, 255, 255, 0, 255, 0, 255, 0]
        """
        row_uncompressed = list()
        number_str = list()
        factor_str = list()
        idx = 0
        n = len(raw_row)

        while idx < n:
            char = raw_row[idx]

            if char >= "0" and char <= "9":
                number_str.append(char)

                if idx == (n-2) and raw_row[idx+1] == "\n" or idx == (n-1):
                    num = int("".join(number_str))
                    row_uncompressed.append(num)

                    number_str = list()
            elif char == ",":
                num = int("".join(number_str))
                row_uncompressed.append(num)

                number_str = list()
            elif char == "[":
                idx += 1

                while raw_row[idx] != "]" and idx < n:
                    factor_str.append(raw_row[idx])
                    idx += 1
                num = int("".join(number_str))
                factor = int("".join(factor_str))

                row_uncompressed += [num] * factor

                number_str = list()
                factor_str = list()
            elif char == "\n":
                pass
            else:
                print(f"symbol not supported: {char}")
                raise Exception("Error trying to read image, corrupted file!") 

            idx += 1

        return row_uncompressed

    def __compress(self, row: list) -> str:
        """Given a row with the pixels, generate the compressed version of the raw row (as string).

        EXAMPLE:
        Input: [ [0, 0, 0], [255, 255, 255], [255, 0, 255], [0, 255, 0]]
        Expected: "0[3]255[4]0,255,0,255,0"
        """
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

        if factor > 1:
            compressed_row.append(f"{reference_value}[{factor}]")
        elif "]" in compressed_row[-1]:
            compressed_row.append(str(reference_value))
        else:
            compressed_row.append(f",{reference_value}")

        return "".join(compressed_row)
