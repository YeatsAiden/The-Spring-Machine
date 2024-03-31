from settings import *
from core_funcs import *
from animation import Animation

class Entity():
    def __init__(self, image_path: str, pos: list[int]):
        self.flip: bool = False

        self.animation_config: dict[str, dict]
        self.animation: dict[str, Animation]

        self.image : pg.Surface

        self.pos = pos
        self.rect : pg.FRect | pg.Rect       

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
        