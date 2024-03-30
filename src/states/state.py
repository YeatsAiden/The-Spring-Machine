from core_funcs import*
from settings import *


class State:
    def __init__(self) -> None:
        self.exit = False
        self.quit = False
        self.next_state = None
    

    def update(self, dt: float):
        pass


    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2):
        pass


    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exit = True