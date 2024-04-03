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

from math import dist


class Flowey(Entity):
    def __init__(self, image_path: str, pos):
        super().__init__(image_path, pos)
        self.state = "cute"

        self.animation_config: dict[str, dict] = {dir: load_json(image_path + "/" + dir + "/" + dir + ".json") for dir in get_dir_names(image_path)}
        self.animation: dict[str, Animation] = {dir: Animation(image_path + "/" + dir + "/" + dir + ".png", self.animation_config[dir]) for dir in get_dir_names(image_path)}

        self.pos = pos

        self.activation_range = 5*TILE_SIZE

        self.current_animation: Animation = self.animation[self.state]
        self.image = self.current_animation.image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.time_since_last_attack = 0
        self.cooldown = 2  # secs
        self.time_to_spit_spore = False

    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2):
        self.image = self.current_animation.animate(self.flip)
        surf.blit(self.image, self.rect.topleft - cam_pos)

    def update(self, player_pos, current_time: int, in_bounds: bool):
        self.time_to_spit_spore = False

        if in_bounds:
            if current_time - self.time_since_last_attack > self.cooldown:
                self.time_to_spit_spore = True
                self.time_since_last_attack = current_time

        self.anim_state_check(player_pos)

    def anim_state_check(self, player_pos):
        if dist(player_pos, self.pos) < self.activation_range and self.state == "cute":
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'scary', self.current_animation.animation_index)
        elif dist(player_pos, self.pos) > self.activation_range and self.state == "scary":
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'cute', self.current_animation.animation_index)

        self.current_animation = self.animation[self.state]

    def change_anim_state(self, state, new_state, frame):
        if new_state != state:
            state, frame = new_state, 0
        return state, frame

