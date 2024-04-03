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

from math import sin, cos


class FloweySpore(Entity):
    def __init__(self, image_path: str, pos):
        super().__init__(image_path, pos)
        self.state = "existing"

        self.possible_states = ["existing", "not existing"]


        self.pos = pos
        self.image = pg.image.load(image_path+"/flowey_spore.png")
        self.rect = pg.FRect(self.image.get_bounding_rect())
        self.rect.topleft = self.pos

        self.vel = pg.Vector2(0, -1)
        self.acceleration = 0.5

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2, current_time: float):
        freq = 5
        amplitude = 10
        image = pg.transform.rotate(self.image, cos(current_time*freq)*20)
        spore_pos = image.get_rect(center=self.rect.center).topleft - cam_pos

        spore_pos.x += sin(current_time*freq)*amplitude

        surf.blit(image, spore_pos)

    def move(self, dt: float, rects: dict[str, dict[str, pg.Rect | pg.FRect]], current_time: float, in_bounds: bool, player_pos):
        self.vel.y += self.acceleration * dt
        self.vel.y = min(self.vel.y, 10*dt)

        if player_pos[0] < self.rect.x:
            self.vel.x = -10*dt
        else:
            self.vel.x = 10*dt

        self.movement(rects)

    def collision_check(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]]):
        collide_rects = []
        for layer in rects:
            for rect in rects[layer]:
                if rects[layer][rect].colliderect(self.rect):
                    collide_rects.append(rects[layer][rect])

        return collide_rects

    def movement(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]]):
        self.rect.x += self.vel.x
        if len(self.collision_check(rects)) > 0:
            self.state = "not existing"

        self.rect.y += self.vel.y
        if len(self.collision_check(rects)) > 0:
            self.state = "not existing"
