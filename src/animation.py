from settings import *
from core_funcs import *


class Animation:
    def __init__(self, animation_path: str) -> None:
        self.animation: list[pg.Surface] = self.load_animation(animation_path)
        self.image: pg.Surface = self.animation[0]
        self.animation_index: int = 0

        self.freeze_time: bool = False
        self.freeze: bool = False
        self.time_since_freeze: float = 0


    def load_animation(self, path: str, durations):
        animation_name = path.split("/")[-1]
        animation = []

        for index, frames in enumerate(durations):
            img_name = animation_name + "_" + str(index)
            img_path = path + "/" + img_name + ".png"
            img = pg.image.load(img_path).convert_alpha()
            for frame in range(frames):
                animation.append(img)
        
        return animation
    

    def animate(self, flip: bool):
        self.animation_index += 1
        self.animation_index = 0 if self.animation_index == len(self.animation) else self.animation_index
        image = pg.transform.flip(self.image, flip, False)
        return image
