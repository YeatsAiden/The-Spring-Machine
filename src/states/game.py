
try:
    from settings import *
    from ui import *
    from level import Level
    from player import Player
except:
    from src.settings import *
    from src.ui import *
    from src.level import Level
    from src.player import Player
from .state import State


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

        self.player = Player(PATHS["player"], [50, -100])
    

    def update(self, dt: float, keys_pressed, current_time: float):
        self.cam_pos.x += (self.player.rect.x - self.cam_pos.x - DISPLAY_WIDTH/2)/10
        self.cam_pos.y += (self.player.rect.y - self.cam_pos.y - DISPLAY_HEIGHT/2)/10

        self.tile_area = self.levels["0"].get_area(self.cam_pos)
        self.rect_area = self.levels["0"].get_rects(self.tile_area)

        self.player.move(keys_pressed, dt, self.rect_area, current_time)


    def draw(self, surf: pg.Surface):
        surf.fill("black")
        self.levels["0"].draw_level(surf, self.tile_area, self.cam_pos)
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