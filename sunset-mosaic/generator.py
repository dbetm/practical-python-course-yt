import os
import random
from datetime import datetime

import pandas as pd
from PIL import Image
from tqdm import tqdm

from constants import DIM_WINDOW, NUM_IMGS_PER_ROW, OUTPUT_DATASET_PATH
from images import compute_nearest_images, get_average_per_channel, resize_img
from utils import open_dataset


def generate(target_img: Image) -> Image:
    target_img = resize_img(target_img, DIM_WINDOW*NUM_IMGS_PER_ROW)

    n, m = target_img.height, target_img.width
    for y in tqdm(range(0, n, DIM_WINDOW)):
        for x in range(0, m, DIM_WINDOW):
            left = x
            upper = y
            right = min(m-1, x+DIM_WINDOW)
            lower = min(n-1, y+DIM_WINDOW)

            window = target_img.crop((left, upper, right, lower))

            avg = get_average_per_channel(window)
            nearest_image_names = compute_nearest_images(metadata, avg, k=3)

            selected_img_name = random.choice(nearest_image_names)

            for i in enumerate(range(upper, lower)):
                for j in enumerate(range(left, right)):
                    new_pixel = images_in_memory[selected_img_name].getpixel((j[0], i[0]))

                    target_img.putpixel((j[1], i[1]), value=new_pixel)

    return target_img



if __name__ == "__main__":
    images_in_memory = open_dataset(OUTPUT_DATASET_PATH)

    filename = "mona_lisa.jpg"
    testing_img_filepath = f"assets/{filename}"
    output_path = "outputs"

    metadata = pd.read_csv("sunset_metadata.csv")

    with Image.open(testing_img_filepath) as img:
        mosaic_image = generate(img)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        mosaic_image.save(os.path.join(output_path, f"out_{timestamp}_{filename}"))

