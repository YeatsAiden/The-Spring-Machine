from state_manager import StateManager
from settings import *

# Initial setup
pg.init()

window = pg.display.set_mode(WINDOW_SIZE, FLAGS)
display = pg.Surface(DISPLAY_SIZE)
clock = pg.time.Clock()
pg.mouse.set_visible(MOUSE_VISIBLE)

manager = StateManager(display, window, clock)
# lol
manager.run()
