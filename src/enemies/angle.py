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

from math import sin, dist

class Angel(Entity):
    def __init__(self, image_path: str, pos):
        super().__init__(image_path, pos)
        self.state = "idle"

        self.animation_config = load_json(image_path + "/angle/angle.json")
        self.animation = Animation(image_path + "/angle/angle.png", self.animation_config)

        self.pos = pos
        self.current_animation = self.animation
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

        self.vision_radius = 4 * TILE_SIZE
        self.camp_height = 3 * TILE_SIZE

        self.last_bomb_spawn_time = 0
        self.bomb_spawn_cooldown = 5  # secs
        self.time_to_spawn_a_bomb = False

    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2, current_time):
        self.image = self.current_animation.animate(self.flip)

        angle_pos = self.rect.topleft - cam_pos
        angle_pos.y += sin(current_time*5)*2

        surf.blit(self.image, angle_pos)

    def move(self, dt: float, rects: dict[str, dict[str, pg.Rect | pg.FRect]], current_time: float, in_bounds: bool, player_pos):
        if in_bounds:
            if self.state == "following player":
                if player_pos[0]+5 < self.rect.centerx:
                    self.vel.x = -20*dt
                elif player_pos[0]-5 > self.rect.centerx:
                    self.vel.x = 20*dt
                else:
                    self.vel.x = 0

                if (player_pos[1] - self.camp_height + 5) < self.rect.centery:
                    self.vel.y = -40*dt
                elif (player_pos[1] - self.camp_height - 5) > self.rect.centery:
                    self.vel.y = 40*dt
                else:
                    self.vel.y = 0
            else:
                self.vel.x = 0
                self.vel.y = 0

            self.time_to_spawn_a_bomb = False  # reset every frame

            if current_time - self.last_bomb_spawn_time > self.bomb_spawn_cooldown and self.state == "following player":
                self.last_bomb_spawn_time = current_time
                self.time_to_spawn_a_bomb = True

            self.movement(rects)

        self.anim_state_check(player_pos)

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
            elif self.vel.y < 0:
                self.collision_state["top"] = True
                self.vel.y = 0
                self.rect.top = rect.bottom

    def anim_state_check(self, player_pos):
        if dist(player_pos, self.rect.center) < self.vision_radius:
            self.state = "following player"
        else:
            self.state = "idle"

        if self.state == "following player":
            if player_pos[0] > self.rect.centerx:
                self.flip = True
            else:
                self.flip = False

    @staticmethod
    def change_anim_state(state, new_state, frame):
        if new_state != state:
            state, frame = new_state, 0
        return state, frame
