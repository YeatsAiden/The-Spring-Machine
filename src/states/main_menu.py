from src.core_funcs import *
from src.settings import *
from .state import State
from src.ui import *


class MainMenu(State):
    def __init__(self) -> None:
        super().__init__(show_cursor=True)
        self.done = False
        self.next_state = None

        self.smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)

        # main menu
        self.play_button = Button("assets/ui/buttons/button.png")
        self.play_button.set_position((DISPLAY_WIDTH-self.play_button.rect.w)//2, 100)


    def update(self, *args):
        dt = args[0]
        current_time = args[1]
        mouse_pos = args[2]

        play_clicked = self.play_button.check_click(mouse_pos, pg.mouse.get_pressed(), current_time)

        if play_clicked:
            print("helloooo")


    def draw(self, *args):
        surf = args[0]
        font = args[1]

        surf.fill("black")
        self.play_button.draw(surf, font)


    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit = True
