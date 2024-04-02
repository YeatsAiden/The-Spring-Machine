from settings import *
from core_funcs import *
from entity import Entity
from animation import Animation

class Player(Entity):
    def __init__(self, image_path: str, pos):
        super().__init__(image_path, pos)
        self.flip = False
        self.state = "idle"

        self.animation_config: dict[str, dict] = {dir: load_json(image_path + "/" + dir + "/" + dir + ".json") for dir in get_dir_names(image_path)}
        self.animation: dict[str, Animation] = {dir: Animation(image_path + "/" + dir + "/" + dir + ".png", self.animation_config[dir]) for dir in get_dir_names(image_path)}

        self.pos = pos
        self.current_animation: Animation = self.animation[self.state]
        self.image = self.current_animation.image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.acceleration: int = 5
        self.max_vel: int = 20
        self.min_vel: int = 1
        self.friction: float = 1.05

        self.max_fall_speed: int = 20
        self.g: float = 9.8
        self.mass = 1
        self.jump_force = 6
        self.vel = pg.Vector2(0, 0)
        self.momentum = pg.Vector2(0, 0)

        self.input_states = {
            "moving": False,
            "jumping": False,
            "crouching": False
        }

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


    def move(self, keys_pressed, dt: float, rects: dict[str, dict[str, pg.Rect | pg.FRect]], current_time: float):

        move_right = keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]
        move_left = keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]
        jump = keys_pressed[pg.K_UP] or keys_pressed[pg.K_SPACE] or keys_pressed[pg.K_w]
        crouch = keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]

        self.input_states["moving"] = True if move_right or move_left else False
        self.input_states["jumping"] = True if jump else False
        self.input_states["crouching"] = True if crouch else False

        self.vel.x += self.acceleration * dt * (move_right - move_left)

        if jump:
            self.vel.y = 0
            self.vel.y -= self.jump_force * dt * 20
        
        if not self.collision_state["bottom"]:
            self.vel.y += self.g * self.mass * dt

        if not self.input_states["moving"]:
            self.vel.x /= self.friction
        if abs(self.vel.x) < self.min_vel and not self.input_states["moving"]:
            self.vel.x = 0


        self.vel.y = min(self.vel.y, self.max_fall_speed)
        self.vel.x = min(self.vel.x, self.max_vel)

        self.movement(rects, current_time)
        self.anim_state_check(keys_pressed)

        
    def wall_jump(self, dt):
        can_wall_jump = (self.collision_state['right'] or self.collision_state['left']) and not self.collision_state['bottom']
        if self.player_input_state['jumping'] and (self.player_input_state['moving_right'] or self.player_input_state['moving_left']) and can_wall_jump:
            self.momentum.y = 0
            self.momentum.y -= self.jump_force * dt
            self.momentum.x += 100 * dt * (self.collision_state['left'] - self.collision_state['right'])


    def collision_check(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]]):
        collide_rects = []
        for layer in rects:
            for rect in rects[layer]:
                if rects[layer][rect].colliderect(self.rect):
                    collide_rects.append(rects[layer][rect])

        return collide_rects


    def movement(self, rects: dict[str, dict[str, pg.Rect | pg.FRect]], current_time: float):
        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }
                    
        self.rect.x += self.vel.x
        for rect in self.collision_check(rects):
            if self.vel.x > 0:
                self.collision_state["right"] = True
                self.vel.x = 0
                self.rect.right = rect.left
                self.time_since_last_collision = time.time()
            elif self.vel.x < 0:
               self.collision_state["left"] = True
               self.vel.x = 0
               self.rect.left = rect.right
               self.time_since_last_collision = time.time()

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
                self.time_since_last_collision = time.time()


    def anim_state_check(self, keys_pressed):
        move_right = keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]
        move_left = keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]

        if self.vel.x == 0 and self.vel.y == 0:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, "idle", self.current_animation.animation_index)

        if self.input_states['moving'] and self.collision_state['bottom'] and not (self.collision_state['right'] or self.collision_state['left']):
            
            self.state, self.current_animation.animation_index = 'run', self.current_animation.animation_index

        if self.input_states['jumping']:
            self.state, self.current_animation.animation_index = 'jump', self.current_animation.animation_index

        if self.vel.y < 0 and not self.collision_state["bottom"]:
            self.state, self.current_animation.animation_index = 'fly', self.current_animation.animation_index

        if not self.collision_state["bottom"] and self.vel.y > 0:
            self.state, self.current_animation.animation_index = 'fall', self.current_animation.animation_index

        if ((move_right and self.vel.x < 0) or (move_left and self.vel.x > 0)) and self.collision_state['bottom']:
            self.state, self.current_animation.animation_index = 'skid', self.current_animation.animation_index

        if self.vel.x > 0:
            self.flip = False
        elif self.vel.x < 0:
            self.flip = True

        self.flip = not self.flip if self.state == 'skid' else self.flip
        
        self.current_animation = self.animation[self.state]
    

    def change_anim_state(self, state, new_state, frame):
        if new_state != state:
            state, frame = new_state, 0
        return state, frame