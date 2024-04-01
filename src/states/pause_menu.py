from core_funcs import *
from settings import *
from .state import State

class PauseMenu(State):
    def __init__(self) -> None:
        super().__init__()
        self.done = False
        self.next_state = None
    

    def update(self, *args):
        dt = args[0]
        pass


    def draw(self, *args):
        surf = args[0]
        pass


    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                    self.next_state = "Game"
            