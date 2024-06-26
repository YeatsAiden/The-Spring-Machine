try:
    from settings import *
    from core_funcs import *
    from entity import Entity
    from animation import Animation
    from particle import Particle
except:
    from src.settings import *
    from src.core_funcs import *
    from src.entity import Entity
    from src.animation import Animation
    from src.particle import Particle

from math import sin


class AngelBomb(Entity):
    def __init__(self, image_path: str, pos):
        super().__init__(image_path, pos)
        self.state = "not exploded (nice)"

        self.possible_states = ["not exploded (nice)", "exploding (not nice)", "done exploding"]

        self.animation_config = load_json(image_path + "/angle_bomb/angle_bomb.json")
        self.animation = Animation(image_path + "/angle_bomb/angle_bomb.png", self.animation_config)

        self.pos = pos
        self.current_animation = self.animation
        self.image = self.current_animation.image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.vel = pg.Vector2(0, 0)
        self.moving_speed = 10
        self.acceleration = 2

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

        self.particle = Particle()
        self.particle.create_proccess("explosion", 2, True, False, False, 60, 0.05)

    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2, current_time: float, dt: float, rect_area):
        if self.state == "not exploded (nice)":
            self.image = self.current_animation.animate(self.flip)

            image = pg.transform.scale_by(self.image, 1+sin(current_time*10)/10)
            rect = image.get_rect(center=self.rect.center)
            pos = rect.topleft - cam_pos

            surf.blit(image, pos)
        else:
            particle = [
                [self.rect.x, self.rect.y],
                [random.randint(-30, 30), random.randint(-30, 30)],
                random.randint(10, 20) ,
                0.05,
                3,
                pg.FRect(self.rect.x, self.rect.y, 1, 1),
                pg.image.load(PATHS["particle"] + '/smoke.png').convert_alpha()
            ]
            self.particle.particle_process(surf, particle, "explosion", cam_pos, rect_area, current_time, dt)

    def move(self, dt: float, rects: dict[str, dict[str, pg.Rect | pg.FRect]], current_time: float, in_bounds: bool):
        self.vel.y = self.moving_speed * dt
        self.moving_speed += self.acceleration

        self.movement(rects)
        self.anim_state_check(in_bounds)

    def collision_check(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]]):
        collide_rects = []
        for layer in rects:
            for rect in rects[layer]:
                if rects[layer][rect].colliderect(self.rect):
                    collide_rects.append(rects[layer][rect])

        return collide_rects

    def movement(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]]):
        self.collision_state["bottom"] = False

        self.rect.y += self.vel.y
        for rect in self.collision_check(rects):
            if self.vel.y > 0:
                self.collision_state["bottom"] = True
                self.vel.y = 0
                self.state = "exploding (not nice)"
                self.rect.bottom = rect.top

    def anim_state_check(self, in_bounds: bool):
        if self.state == "not exploded (nice)" and self.current_animation.animation_index == len(self.current_animation.animation)-1:
            self.state = "exploding (not nice)"
            self.current_animation.animation_index = 0

        if self.state == "exploding (not nice)" and self.current_animation.animation_index == len(self.current_animation.animation)-1:
            self.state = "done exploding"

        if not in_bounds:
            self.state = "done exploding"

    @staticmethod
    def change_anim_state(state, new_state, frame):
        if new_state != state:
            state, frame = new_state, 0
        return state, frame
