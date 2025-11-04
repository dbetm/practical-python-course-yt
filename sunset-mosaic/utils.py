import os
from math import sqrt
from typing import List, Union

from PIL import Image


def open_dataset(dataset_path: str) -> dict: 
    files = os.listdir(path=dataset_path)

    images_in_memory = dict()

    for file in files:
        images_in_memory[file] = Image.open(os.path.join(dataset_path, file))

    return images_in_memory



def compute_euclidian_distance(a: List[Union[int, float]], b: List[Union[int, float]]) -> float:
    """sqrt( Σ (a_i - b_i)² ),   for i = 1 to n"""
    acc = 0.0

    for a_i, b_i in zip(a, b):
        acc += (a_i - b_i)**2

    return sqrt(acc)