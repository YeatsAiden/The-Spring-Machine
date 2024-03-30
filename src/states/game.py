from core_funcs import *
from settings import *
from level import Level
from ui import *
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

        self.tile_area: dict[str, set]
        self.rect_area: dict[str, dict[str, pg.Rect | pg.FRect]]
    

    def update(self, dt: float, cam_pos: pg.Vector2):
        self.tile_area = self.levels["0"].get_area(cam_pos)

    def draw(self, surf: pg.Surface, cam_pos: pg.Vector2):
        self.levels["0"].draw_level(surf, self.tile_area, cam_pos)


    def event_loop(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                    self.next_state = "PauseMenu"