try:
    from settings import *
except:
    from src.settings import *


class State:
    def __init__(self, show_cursor=False) -> None:
        self.exit = False
        self.quit = False
        self.next_state = None

        self.cursor_visible = show_cursor
    

    def update(self, *args):
        pass


    def draw(self, *args):
        pass


    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exit = True
