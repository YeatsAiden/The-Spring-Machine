from settings import *
from core_funcs import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos):
        super().__init__()
        self.animation_frame = 0
        self.flip = False

        self.pos = pos
        self.image = self.animation.animations['idle'][0]
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
        self.image, self.animation_frame = self.animation.animate(self.animation_frame, self.player_state, self.flip)
        surf.blit(self.image, self.rect.topleft - cam_pos)
    

    def move(self, keys_pressed, dt, rects, current_time):
        pass

    def wall_jump(self, dt):
        can_wall_jump = (self.collision_state['right'] or self.collision_state['left']) and not self.collision_state['bottom']
        if self.player_input_state['jumping'] and (self.player_input_state['moving_right'] or self.player_input_state['moving_left']) and can_wall_jump:
            self.momentum.y = 0
            self.momentum.y -= self.jump_force * dt
            self.momentum.x += 100 * dt * (self.collision_state['left'] - self.collision_state['right'])


    def collision_check(self, rects):
        collide_rects = []
        for rect in rects:
            if rect.colliderect(self.rect):
                collide_rects.append(rect)
        
        return collide_rects
    

    def collision_state_check(self, rects, tile_size):
        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }


        self.rect.x += self.vel.x
        if self.vel.x > 0:
            x = self.rect.right // tile_size
            y = self.rect.bottom // tile_size
        elif self.vel.x < 0:
            x = self.rect.left // tile_size
            y = self.rect.bottom // tile_size

        self.rect.y += self.vel.y
            
    

    def player_state_check(self, keys_pressed):
        if self.momentum.x == 0 and self.momentum.y == 0:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'idle', self.animation_frame)

        if (self.player_input_state['moving_right'] or self.player_input_state['moving_left']) and self.collision_state['bottom'] and not (self.collision_state['right'] or self.collision_state['left']):
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'run', self.animation_frame)

        if self.player_input_state['jumping']:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'jump', self.animation_frame)

        if self.momentum.y < 0 and not self.collision_state["bottom"]:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'fly', self.animation_frame)

        if not self.collision_state["bottom"] and self.momentum.y > 0:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'fall', self.animation_frame)

        if (((self.player_input_state['moving_right']) and self.momentum.x < 0) or ((self.player_input_state['moving_left']) and self.momentum.x > 0)) and self.collision_state['bottom']:
            self.player_state, self.animation_frame = self.animation.change_state(self.player_state, 'skid', self.animation_frame)
        
        if self.momentum.x > 0:
            self.flip = False
        elif self.momentum.x < 0:
            self.flip = True

    def timer(self, current_time, previous_time, cool_down):
        return current_time - previous_time > cool_down
        