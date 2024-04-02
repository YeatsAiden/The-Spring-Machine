try:
    from settings import *
    from core_funcs import *
    from entity import Entity
    from animation import Animation
except:
    from src.settings import *
    from src.core_funcs import *
    from src.entity import Entity
    from src.animation import Animation


class Flowey(Entity):
    def __init__(self, image_path: str, pos, starting_direction: str = "left"):
        super().__init__(image_path, pos)
        self.direction = starting_direction

        if starting_direction == "idle":
            raise Exception("NO IDLE FOR GLACIERD")

        self.animation_config: dict[str, dict] = {dir: load_json(image_path + "/" + dir + "/" + dir + ".json") for dir in get_dir_names(image_path)}
        self.animation: dict[str, Animation] = {dir: Animation(image_path + "/" + dir + "/" + dir + ".png", self.animation_config[dir]) for dir in get_dir_names(image_path)}

        self.pos = pos
        self.current_animation: Animation = self.animation[self.direction]
        self.image = self.current_animation.image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.vel = pg.Vector2(0, 0)

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

        self.time_since_last_collision: float = 0
        self.collision_cooldown: float = 0.5
