try:
    from settings import *
    from ui import *
    from level import Level
    from player import Player
    from enemies.glacierd import Glacierd
    from enemies.flowey import Flowey
    from enemies.angle import Angel
except:
    from src.settings import *
    from src.ui import *
    from src.level import Level
    from src.player import Player
    from src.enemies.angle import Angel

from .state import State
import random


class Game(State):
    def __init__(self) -> None:
        super().__init__()
        self.done: bool = False
        self.next_state: str = None

        self.objects: dict[str, pg.Surface] = load_images(PATHS["objects"])
        self.spawns: dict[str, pg.Surface] = load_images(PATHS["spawns"])
        self.tile_sets: dict[str, dict[int, pg.Surface]] = {file.split('.')[0]: make_tileset_dict(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "png"}
        self.tile_sets_rules: dict[str, dict[str, int]] = {file.split('.')[0]: load_json(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "json"}

        self.smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)

        self.levels: dict[str, Level] = {file.split('.')[0]: Level(self.objects, self.spawns, self.tile_sets, PATHS['levels'] + "/" + file) for file in get_file_names(PATHS['levels']) if file.split('.')[1] == "json"}

        self.tile_area: dict[str, dict[str, pg.Rect | pg.FRect]]
        self.rect_area: dict[str, dict[str, pg.Rect | pg.FRect]]

        self.cam_pos = pg.Vector2(0, 0)

        self.player = Player(PATHS["player"], [100, -100])

        self.glacierd_test = Glacierd(PATHS["enemies"]+"/glacierd", [200, 50], "up")
        self.flowey_test = Flowey(PATHS["enemies"] + "/flowey", [200, 110])
        self.angle_test = Angel(PATHS["enemies"], [200, 50], "left")

        self.music_playing = random.choice(["melting-through", "breaking-ice"])
    

    def update(self, *args):
        dt = args[0]
        current_time = args[1]
        keys_pressed = args[3]
        sound_manager = args[4]

        sound_manager.play_music(self.music_playing, 0)

        self.cam_pos.x += (self.player.rect.x - self.cam_pos.x - DISPLAY_WIDTH/2)/10
        self.cam_pos.y += (self.player.rect.y - self.cam_pos.y - DISPLAY_HEIGHT/2)/10


        self.tile_area = self.levels["0"].get_area(self.cam_pos)
        self.rect_area = self.levels["0"].get_rects(self.tile_area)

        self.player.move(keys_pressed, dt, self.rect_area, current_time)
        self.glacierd_test.move(dt, self.rect_area, current_time)
        self.flowey_test.update(self.player.rect.center, current_time)
        self.angle_test.move(dt, self.rect_area, current_time)

    def draw(self, *args):
        surf = args[0]

        surf.fill("#4f8fba")
        self.levels["0"].draw_level(surf, self.tile_area, self.cam_pos)

        self.glacierd_test.draw(surf, self.cam_pos)
        self.flowey_test.draw(surf, self.cam_pos)
        self.angle_test.draw(surf, self.cam_pos)

        self.player.draw(surf, self.cam_pos)


    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                    self.next_state = "PauseMenu"
