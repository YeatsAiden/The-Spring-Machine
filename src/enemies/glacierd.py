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


class Glacierd(Entity):
    def __init__(self, image_path: str, pos, starting_direction: str = "left"):
        super().__init__(image_path, pos)
        self.state = starting_direction

        # turn - from right to left and vise versa
        # flip - from up to down and vise versa
        # i am great at naming conventions
        self.possible_states = ["left", "right", "up", "down", "turn", "flip", "turn-back", "flip-back"]

        if starting_direction not in self.possible_states:
            raise Exception("NO IDLE FOR GLACIERD")

        self.animation_config: dict[str, dict] = {dir: load_json(image_path + "/" + dir + "/" + dir + ".json") for dir in get_dir_names(image_path)}
        self.animation: dict[str, Animation] = {dir: Animation(image_path + "/" + dir + "/" + dir + ".png", self.animation_config[dir]) for dir in get_dir_names(image_path)}

        # specifically for glacierd, we have to add 2 extra animations
        self.animation_config.update({"turn-back": load_json(image_path + "/turn/turn.json")})
        self.animation.update({"turn-back": Animation(image_path + "/turn/turn.png", self.animation_config["turn-back"], "reversed")})

        self.animation_config.update({"flip-back": load_json(image_path + "/flip/flip.json")})
        self.animation.update({"flip-back": Animation(image_path + "/flip/flip.png", self.animation_config["flip-back"], "reversed")})


        self.pos = pos
        self.current_animation: Animation = self.animation[self.state]
        self.image = self.current_animation.image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.vel = pg.Vector2(0, 0)
        self.moving_speed = 10

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
        if self.state in ["left", "turn-back"]:
            self.vel.x = -self.moving_speed * dt
        elif self.state in ["right", "turn"]:
            self.vel.x = self.moving_speed * dt
        elif self.state in ["up", "flip-back"]:
            self.vel.y = -self.moving_speed * dt
        else:
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
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'turn', self.current_animation.animation_index)

        if self.collision_state['right']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'turn-back', self.current_animation.animation_index)

        if self.collision_state['top']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'flip', self.current_animation.animation_index)

        if self.collision_state['bottom']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'flip-back', self.current_animation.animation_index)


        if self.state in ["turn", "turn-back", "flip", "flip-back"]:
            if self.current_animation.animation_index == len(self.current_animation.animation)-1:
                if self.state == "turn":
                    self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'right', self.current_animation.animation_index)
                elif self.state == "turn-back":
                    self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'left', self.current_animation.animation_index)
                elif self.state == "flip":
                    self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'down', self.current_animation.animation_index)
                elif self.state == "flip-back":
                    self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'up', self.current_animation.animation_index)

        self.current_animation = self.animation[self.state]

    @staticmethod
    def change_anim_state(state, new_state, frame):
        if new_state != state:
            state, frame = new_state, 0
        return state, frame
