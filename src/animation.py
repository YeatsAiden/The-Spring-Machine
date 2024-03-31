from settings import *
from core_funcs import *


class Animation:
    def __init__(self, spritesheet_path: str, config: dict = None) -> None:
        self.spritesheet_path = spritesheet_path
        self.config = config

        if self.config == None:
            raise Exception("WHERE CONFIG >>::(((")
        else:
            self.animation: list[pg.Surface] = self.load_animation(self.spritesheet_path, self.config)

        self.image: pg.Surface = self.animation[0]
        self.animation_index: int = 0

        self.freeze_time: bool = False
        self.freeze: bool = False
        self.time_since_freeze: float = 0


    def load_animation(self, img_path: str, config: dict):
        sprite_sheet = pg.image.load(img_path)
        animation = []

        for index, frame in enumerate(config["frames"]):
            img_data = config["frames"][frame]["frame"]
            img = clip_img(sprite_sheet, img_data["x"], img_data["y"], img_data["w"], img_data["h"])
            for _ in range(int(config["frames"][frame]["duration"]/1000*FPS)):
                animation.append(img)
        
        return animation
    

    def animate(self, flip: bool):
        self.animation_index += 1
        self.animation_index = 0 if self.animation_index == len(self.animation) else self.animation_index
        image = pg.transform.flip(self.animation[self.animation_index], flip, False)
        return image
