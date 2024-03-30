from core_funcs import *
from settings import *
from states.main_menu import MainMenu
from states.game import Game
from states.pause_menu import PauseMenu


class StateManager:
    def __init__(self, display, window, clock) -> None:
        self.display: pg.Surface = display
        self.window = window
        self.clock: pg.Clock = clock

        self.states = {
            "MainMenu": MainMenu,
            "PauseMenu": PauseMenu,
            "Game": Game
        }
        self.current_state: str = "Game"
        self.state = self.states[self.current_state]()
        self.previous_state: str = None

        self.cam_pos = pg.Vector2(0, 0)
        self.xy_change = [0, 0]
        self.scale = 1

        self.current_time = time.time()
        self.dt = 1

        self.full_screen: bool = FULL_SCREEN
        self.fps: int = FPS
    

    def update(self, dt: float, cam_pos: pg.Vector2):
        self.state.update(dt, cam_pos)


    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2):
        self.state.draw(surf, cam_pos)

    
    def event_loop(self, events):
        self.state.event_loop(events)
        # common event loop
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:
                    self.full_screen = not self.full_screen
                    pg.display.set_mode((0, 0), FLAGS | pg.FULLSCREEN) if self.full_screen else pg.display.set_mode(WINDOW_SIZE, FLAGS)

    
    def swap_state(self):
        if self.state.quit:
            pg.quit()
            sys.exit()
        if self.state.done:
            self.state.done = False
            self.previous_state = self.current_state
            self.current_state = self.state.next_state
            self.state = self.states[self.current_state]


    def run(self):
        while True:
            events = pg.event.get()
            self.event_loop(events)
            self.update(self.dt, self.cam_pos)
            self.draw(self.display, self.cam_pos)
            display_cp, self.xy_change, self.scale = resize_surface(self.window, self.display)
            self.window.blit(display_cp, self.xy_change)
            pg.display.update()
            self.dt = self.clock.tick(FPS) / 1000
        