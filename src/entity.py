from settings import *
from core_funcs import *
from animation import Animation

class Entity():
    def __init__(self, image_path: str, pos: list[int]):
        self.flip: bool = False

        self.animation_config: dict[str, dict] = {dir: load_json(image_path + "/" + dir + "/" + dir + ".json") for dir in get_dir_names(image_path)}
        self.animation: dict[str, Animation] = {dir: Animation(image_path + "/" + dir + "/" + dir + ".png", self.animation_config[dir]) for dir in get_dir_names(image_path)}

        self.image = self.animation[list(self.animation)[0]].image

        self.pos = pos
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())        

        self.vel = pg.Vector2(0, 0)

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

        self.state: str


    def draw(self, surf, cam_pos):
        pass
    

    def move(self, dt, rects):
        pass
        