from settings import *
from core_funcs import *
from entity import Entity
from animation import Animation

class Player(Entity):
    def __init__(self, image_path, pos):
        super().__init__(image_path, pos)
        self.flip = False

        self.animation_config: dict[str, dict] = {dir: load_json(image_path + "/" + dir + "/" + dir + ".json") for dir in get_dir_names(image_path)}
        self.animation: dict[str, Animation] = {dir: Animation(image_path + "/" + dir + "/" + dir + ".png", self.animation_config[dir]) for dir in get_dir_names(image_path)}

        self.pos = pos
        self.image = self.animation["idle"].image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.acceleration = 5
        self.vel = pg.Vector2(0, 0)

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

        self.player_state = "idle"


    def draw(self, surf, cam_pos):
        pass


    def move(self, keys_pressed, dt, rects, current_time):
        pass
        