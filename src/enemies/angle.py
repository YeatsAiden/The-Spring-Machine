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

from math import sin

class Angel(Entity):
    def __init__(self, image_path: str, pos, starting_state: str = "idle"):
        super().__init__(image_path, pos)
        self.state = starting_state

        self.possible_states = ["left", "right", "up", "down", "idle"]

        self.animation_config = load_json(image_path + "/angle/angle.json")
        self.animation = {"left": Animation(image_path + "/angle/angle.png", self.animation_config),
                          "right": Animation(image_path + "/angle/angle.png", self.animation_config, "flipped"),
                          "up": Animation(image_path + "/angle/angle.png", self.animation_config),
                          "down": Animation(image_path + "/angle/angle.png", self.animation_config, "flipped"),
                          "idle": Animation(image_path + "/angle/angle.png", self.animation_config)}

        self.pos = pos
        self.current_animation: Animation = self.animation[self.state]
        self.image = self.current_animation.image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.vel = pg.Vector2(0, 0)
        self.moving_speed = 20

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

        self.time_since_last_collision: float = 0
        self.collision_cooldown: float = 0.5

    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2):
        self.image = self.current_animation.animate(self.flip)
        surf.blit(self.image, self.rect.topleft - cam_pos)

    def move(self, dt: float, rects: dict[str, dict[str, pg.Rect | pg.FRect]], current_time: float):
        if self.state == "left":
            self.vel.x = -self.moving_speed * dt
        elif self.state == "right":
            self.vel.x = self.moving_speed * dt
        elif self.state == "up":
            self.vel.y = -self.moving_speed * dt
        elif self.state == "down":
            self.vel.y = self.moving_speed * dt

        self.movement(rects)
        self.anim_state_check()

    def collision_check(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]]):
        collide_rects = []
        for layer in rects:
            for rect in rects[layer]:
                if rects[layer][rect].colliderect(self.rect):
                    collide_rects.append(rects[layer][rect])

        return collide_rects

    def movement(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]]):
        self.collision_state["right"] = False
        self.collision_state["left"] = False
        self.collision_state["top"] = False
        self.collision_state["bottom"] = False

        self.rect.x += self.vel.x
        for rect in self.collision_check(rects):
            if self.vel.x > 0:
                self.collision_state["right"] = True
                self.vel.x = 0
                self.rect.right = rect.left
            elif self.vel.x < 0:
                self.collision_state["left"] = True
                self.vel.x = 0
                self.rect.left = rect.right

        self.rect.y += self.vel.y
        for rect in self.collision_check(rects):
            if self.vel.y > 0:
                self.collision_state["bottom"] = True
                self.vel.y = 0
                self.rect.bottom = rect.top
                self.time_since_last_collision = time.time()
            elif self.vel.y < 0:
                self.collision_state["top"] = True
                self.vel.y = 0
                self.rect.top = rect.bottom

    def anim_state_check(self):
        if self.collision_state['left']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'right', self.current_animation.animation_index)

        if self.collision_state['right']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'left', self.current_animation.animation_index)

        if self.collision_state['top']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'down', self.current_animation.animation_index)

        if self.collision_state['bottom']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'up', self.current_animation.animation_index)

        self.current_animation = self.animation[self.state]

    @staticmethod
    def change_anim_state(state, new_state, frame):
        if new_state != state:
            state, frame = new_state, 0
        return state, frame
