import os
from typing import Generator

import numpy as np
from moviepy import ImageClip, concatenate_videoclips
from numpy.typing import NDArray
from PIL import Image


class Timelapse:
    def __init__(self, frames_path: str, fps: int = 30):
        self.fps = fps
        self.frames_path = frames_path

    def __load_frame(self, images_path: str) -> Generator[NDArray, None, None]:
        filenames = [
            filename
            for filename in os.listdir(images_path)
            if not filename.startswith(".")
        ]

        filenames.sort(key=lambda name: int(name.split("_")[0]))

        for img_filename in filenames:
            img_filepath = os.path.join(images_path, img_filename)
            yield np.array(Image.open(img_filepath), np.uint8)

    def make(self, output_filepath: str):
        frames = list()
        duration_per_frame = 1 / self.fps

        assert output_filepath.endswith(".mp4"), "format for output video must be .mp4"

        for frame in self.__load_frame(self.frames_path):
            frames.append(ImageClip(frame, duration=duration_per_frame))

        video = concatenate_videoclips(frames)

        # save video, maybe you need to install ffmpeg in your computer
        video.write_videofile(output_filepath, fps=self.fps, codec="libx264")
