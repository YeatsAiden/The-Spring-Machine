from settings import *
from core_funcs import *

class Entity():
    def __init__(self, image_path: str, pos: pg.Vector2):
        self.animation_frame: int = 0
        self.flip: bool = False

        self.pos = pos
        self.rect = pg.FRect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())        

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
        