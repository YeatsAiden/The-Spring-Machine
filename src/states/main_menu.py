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
        super().__init__(show_cursor=True)
        self.done = False
        self.next_state = None

        self.smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)

        # main menu
        play_button_hover_anim = Animation(current_dir + "/assets/ui/buttons/normal/button-sheet.png", load_json(current_dir + "/assets/ui/buttons/normal/button.json"), loop_type="linear")
        play_reversed_button_hover_anim = Animation(current_dir + "/assets/ui/buttons/normal/button-sheet.png", load_json(current_dir + "/assets/ui/buttons/normal/button.json"), loop_type="reversed linear")

        settings_button_hover_anim = Animation(current_dir + "/assets/ui/buttons/normal/button-sheet.png", load_json(current_dir + "/assets/ui/buttons/normal/button.json"), loop_type="linear")
        settings_reversed_button_hover_anim = Animation(current_dir + "/assets/ui/buttons/normal/button-sheet.png", load_json(current_dir + "/assets/ui/buttons/normal/button.json"), loop_type="reversed linear")

        self.play_button = Button(play_reversed_button_hover_anim,
                                  play_button_hover_anim,
                                  play_button_hover_anim.animation[-1].copy(),
                                  play_button_hover_anim.animation[0].get_rect(center=(DISPLAY_WIDTH // 2, 100)),
                                  "play",
                                  (13, 5),
                                  2)

        self.settings_button = Button(settings_reversed_button_hover_anim,
                                      settings_button_hover_anim,
                                      settings_button_hover_anim.animation[-1].copy(),
                                      settings_button_hover_anim.animation[0].get_rect(center=(DISPLAY_WIDTH // 2, 130)),
                                      "settings",
                                      (7, 5),
                                      1.4)

    def update(self, *args):
        dt = args[0]
        current_time = args[1]
        mouse_pos = args[2]

        self.play_button.update(mouse_pos, pg.mouse.get_pressed(), current_time)
        self.settings_button.update(mouse_pos, pg.mouse.get_pressed(), current_time)

        if self.play_button.pressed:
            self.next_state = "Game"
            self.done = True

        elif self.settings_button.pressed:
            self.next_state = "Settings"
            self.done = True

    def draw(self, *args):
        surf = args[0]

        surf.fill("black")

        self.play_button.draw(surf, self.smol_font)
        self.settings_button.draw(surf, self.smol_font)

    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit = True
