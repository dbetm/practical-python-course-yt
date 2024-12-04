import random
from datetime import datetime

from PIL import Image

from img_utils import get_base_img


MIN_STARS = 20
MAX_STARS = 140
PADDING = 5

STARS_DEFINITION = {
    "square": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "ele": [(0, -1), (0, 0), (1, 0)], # (x, y-1), (x, y), (x+1, y)
    "classic": [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)],
}


def get_bright() -> int:
    partition = random.randint(a=1, b=100)

    if partition <= 5:
        return random.randint(a=60, b=79)

    if partition <= 15:
        return random.randint(a=80, b=99)

    if partition <= 45:
        return random.randint(a=100, b=149)

    if partition <= 85:
        return random.randint(a=150, b=199)

    if partition <= 95:
        return random.randint(a=200, b=249)

    # <= 100
    return random.randint(a=250, b=255)


def generate_starry_img(num_stars: int) -> Image:
    base_img = get_base_img(width=540, height=960)

    for _ in range(num_stars):
        x = random.randint(a=PADDING, b=base_img.width - PADDING)
        y = random.randint(a=PADDING, b=base_img.height - PADDING)

        bright = get_bright()

        pixel_value = (bright, bright, bright)

        star_type = random.sample(sorted(STARS_DEFINITION), k=1)[0]
        deltas = STARS_DEFINITION[star_type]

        for (delta_x, delta_y) in deltas:
            base_img.putpixel(xy=(x+delta_x, y+delta_y), value=pixel_value)

    return base_img


if __name__ == "__main__":

    for x in range(20):
        num_stars = random.randint(MIN_STARS, MAX_STARS)
        datetime_str = datetime.now().strftime("%Y%m%d_%H%M")

        img_path = f"images/{num_stars}_stars_{datetime_str}_{x}.png"

        starry_img = generate_starry_img(num_stars)

        starry_img.save(img_path)