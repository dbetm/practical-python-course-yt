from PIL import Image


def get_base_img(width: int = 600, height: int = 600) -> Image:
    return Image.new("RGB", (width, height), color="black")