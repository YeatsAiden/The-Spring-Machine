from core_funcs import *
from settings import *
from states.main_menu import MainMenu
from states.game import Game
from states.pause_menu import PauseMenu
from music_manager import *


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

        self.xy_change = [0, 0]
        self.scale = 1

        self.mega_cool_bg = pg.image.load(PATHS["backgrounds"] + "/cool-bg.png").convert_alpha()

        self.current_time = time.time()
        self.dt = 1

        self.full_screen: bool = FULL_SCREEN
        self.fps: int = FPS

        self.cursor_image = pg.image.load(PATHS["cursor"]).convert_alpha()
        self.keys_pressed = pg.key.get_pressed()

        # here you can update what music and sfx files are being loaded, note that they are going to be loaded all at one, so maybe this is a potential optimization possibility in the future
        music_list = [PATHS["music"]+"/breaking-ice.wav", PATHS["music"]+"/funkin.wav", PATHS["music"]+"/melting-through.wav"]
        sfx_list = []  # none so far
        self.sound_manager = SoundManager(music_list, sfx_list)


    def update(self, *args):
        dt = args[0]
        keys_pressed = args[1]
        current_time = args[2]
        scale = args[3]
        xy_change = args[4]
        sound_manager = args[5]

        self.state.update(dt, current_time, get_display_mouse_pos(scale, xy_change), keys_pressed, sound_manager)


    def draw(self, surf: pg.Surface, current_time: float, dt: float):
        surf.fill("black")
        self.state.draw(surf, current_time, self.mega_cool_bg, dt)

        if self.state.cursor_visible:
            self.display.blit(self.cursor_image, get_display_mouse_pos(self.scale, self.xy_change))

    
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
            self.state = self.states[self.current_state]()
            self.sound_manager.stop_music()


    def run(self):
        while True:
            self.current_time = time.time()
            self.keys_pressed = pg.key.get_pressed()

            events = pg.event.get()
            self.event_loop(events)
            self.update(self.dt, self.keys_pressed, self.current_time, self.scale, self.xy_change, self.sound_manager)
            self.draw(self.display, self.current_time, self.dt)

            self.swap_state()

            display_cp, self.xy_change, self.scale = resize_surface(self.window, self.display)
            self.window.blit(display_cp, self.xy_change)
            self.dt = self.clock.tick(FPS) / 1000
            pg.display.update()
        