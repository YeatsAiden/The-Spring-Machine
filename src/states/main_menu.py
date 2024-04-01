try:
    from settings import *
    from core_funcs import *
    from ui import *
except:
    from src.settings import *
    from src.core_funcs import *
    from src.ui import *

from .state import State


class MainMenu(State):
    def __init__(self) -> None:
        super().__init__()
        self.done = False
        self.next_state = None

        self.play_button = Button()


    def update(self, dt: float):
        pass


    def draw(self, surf: pg.Surface):
        pass


    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit = True