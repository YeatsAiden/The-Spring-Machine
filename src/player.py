from settings import *
from core_funcs import *
from entity import Entity
from animation import Animation

class Player(Entity):
    def __init__(self, image_path: str, pos):
        super().__init__(image_path, pos)
        self.facing: int = 1
        self.flip: bool = False
        self.state: str = "idle"

        self.animation_config: dict[str, dict] = {dir: load_json(image_path + "/" + dir + "/" + dir + ".json") for dir in get_dir_names(image_path)}
        self.animation: dict[str, Animation] = {dir: Animation(image_path + "/" + dir + "/" + dir + ".png", self.animation_config[dir]) for dir in get_dir_names(image_path)}

        self.pos = pos
        self.current_animation: Animation = self.animation[self.state]
        self.image = self.current_animation.image
        self.rect = pg.FRect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.acceleration: int = 5
        self.max_vel: int = 5
        self.min_vel: int = 1
        self.friction: float = 1.05

        self.max_fall_speed: int = 5
        self.g: float = 9.8
        self.mass = 1
        self.jump_force = 12
        self.vel = pg.Vector2(0, 0)

        self.input_states: dict[str, bool] = {
            "moving": False,
            "jumping": False,
            "crouching": False
        }

        self.collision_state: dict[str, bool] = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }
        self.time_since_last_collision: float = 0
        self.collision_cooldown: float = 0.5

        self.actions: dict[str, Action] = {
            "run": Run(),
            "jump": Jump(),
            "wall_jump": WallJump(),
            "long_jump": LongJump()
        }


    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2):
        self.image = self.current_animation.animate(self.flip)
        surf.blit(self.image, self.rect.topleft - cam_pos)
    

    def get_input_state(self, keys_pressed):
        move_right = keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]
        move_left = keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]
        moving = move_right - move_left
        jump = keys_pressed[pg.K_UP] or keys_pressed[pg.K_SPACE] or keys_pressed[pg.K_w]
        crouch = keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]

        return moving, jump, crouch


    def get_facing(self):
        return self.input_states["moving"] if self.input_states["moving"] != 0 else self.facing


    def move(self, keys_pressed, dt: float, rects: dict[str, dict[str, pg.Rect | pg.FRect]], current_time: float):
        self.input_states["moving"], self.input_states["jumping"], self.input_states["crouching"] = self.get_input_state(keys_pressed)

        self.facing = self.get_facing()
        # Run Action
        if self.actions["run"].action_condition(
            self.input_states["moving"],
            current_time
            ):
            self.vel = self.actions["run"].action(dt, self.vel, self.input_states["moving"], self.acceleration)
        # Jump Action
        if self.actions["jump"].action_condition(
            self.input_states["jumping"] and self.collision_state["bottom"] and not self.input_states["crouching"],
            current_time
            ):
            self.vel = self.actions["jump"].action(dt, self.vel, self.jump_force)
        # Wall jump action
        can_wall_jump = (self.collision_state['right'] or self.collision_state['left']) and not self.collision_state['bottom'] and self.input_states['jumping'] and self.input_states['moving'] and timer(current_time, self.time_since_last_collision, self.collision_cooldown)
        if self.actions["wall_jump"].action_condition(
            can_wall_jump,
            current_time
            ):
            self.vel = self.actions["wall_jump"].action(dt, self.vel, self.facing, self.jump_force)
        # Long jump Action
        if self.actions["long_jump"].action_condition(
            self.input_states["crouching"] and self.input_states["jumping"] and self.collision_state["bottom"],
            current_time
            ):
            self.vel = self.actions["long_jump"].action(dt, self.vel, self.facing, self.jump_force)



        if not self.collision_state["bottom"]:
            self.vel.y += self.g * self.mass * dt

        if not self.input_states["moving"]:
            self.vel.x /= self.friction
        if abs(self.vel.x) < self.min_vel and not self.input_states["moving"]:
            self.vel.x = 0

        self.vel.y = min(self.vel.y, self.max_fall_speed)
        self.vel.x = max(min(self.vel.x, self.max_vel), -self.max_vel)

        self.movement(rects)
        self.anim_state_check(keys_pressed, current_time)


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

        self.rect.y += round(self.vel.y)
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


    def anim_state_check(self, keys_pressed, current_time: float):
        move_right = keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]
        move_left = keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]

        if self.vel.x == 0 and self.vel.y == 0:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, "idle", self.current_animation.animation_index)

        if self.input_states['moving'] and self.collision_state['bottom'] and not (self.collision_state['right'] or self.collision_state['left']):
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'run', self.current_animation.animation_index)

        if self.input_states['jumping']:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'jump', self.current_animation.animation_index)

        if self.vel.y < 0 and not self.collision_state["bottom"]:
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'fly', self.current_animation.animation_index)

        if not self.collision_state["bottom"] and self.vel.y > 0 and timer(current_time, self.time_since_last_collision, self.collision_cooldown):
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'fall', self.current_animation.animation_index)

        if ((move_right and self.vel.x < 0) or (move_left and self.vel.x > 0)) and self.collision_state['bottom'] and not self.state == "jump":
            self.state, self.current_animation.animation_index = self.change_anim_state(self.state, 'skid', self.current_animation.animation_index)

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
    

class Action:
    def __init__(self, freeze_duration: float = 0) -> None:
        self.freeze_frame: bool = False
        self.freeze_duration: float = freeze_duration
        self.time_since_freeze: float = 0
    

    def action_condition(self, condition: bool, current_time: float):
        self.freeze_frame, self.time_since_freeze, action_condition = freeze_frame(condition,
                                                            self.freeze_frame,
                                                            self.freeze_duration,
                                                            self.time_since_freeze,
                                                            current_time)
        return action_condition
    

    def action(self):
        pass


class Run(Action):
    def __init__(self, freeze_duration: float = 0) -> None:
        super().__init__(freeze_duration)
    

    def action(self, dt: float, vel: pg.Vector2, moving: int, acceleration: int):
        vel.x += acceleration * dt * moving
        return vel
    

class Jump(Action):
    def __init__(self, freeze_duration: float = 0.2) -> None:
        super().__init__(freeze_duration)
    

    def action(self, dt: float, vel: pg.Vector2, jump_force: int):
        vel.y = 0
        vel.y -= jump_force * dt * 20
        return vel


class WallJump(Action):
    def __init__(self, freeze_duration: float = 0.05) -> None:
        super().__init__(freeze_duration)
    

    def action(self, dt: float, vel: pg.Vector2, facing: int, jump_force: int):
        vel.y = 0
        vel.y -= jump_force * dt * 20
        vel.x += 200 * dt * -facing
        return vel


class LongJump(Action):
    def __init__(self, freeze_duration: float = 0.3) -> None:
        super().__init__(freeze_duration)
    

    def action(self, dt: float, vel: pg.Vector2, facing: int, jump_force: int):
        vel.x += 400 * dt * facing
        vel.y = 0
        vel.y -= jump_force * dt * 10
        return vel

