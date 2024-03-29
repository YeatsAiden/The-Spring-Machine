from settings import *
from core_funcs import *


class Level:
    def __init__(self, objects: dict, spawns: dict, tile_sets: dict, level_path: str) -> None:
        self.level = {}
        with open(level_path) as f:
            level_json_data = json.load(f)
            self.level = level_json_data

        self.types = {
            "tiles": tile_sets,
            "objects": objects,
            "spawns": spawns,
        }

        self.rects = self.make_rects_dict(self.level)
        self.tiles = {layer: set(self.level[layer]) for layer in self.level}

    def make_rects_dict(self, level: dict):
        rects = {}
        for layer in level:
            rects[layer] = {}
            for tile in level[layer]:
                if tile["collision"]:
                    x, y = map(int, tile.split(":"))
                    rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    rects[layer][tile] = rect
        return rects

    def get_area(self, cam_pos: pg.Vector2):
        area = {}

        start_row = int(cam_pos[1] // TILE_SIZE)
        end_row = int((cam_pos[1] + DISPLAY_HEIGHT) // TILE_SIZE) + 1
        start_col = int(cam_pos[0] // TILE_SIZE)
        end_col = int((cam_pos[0] + DISPLAY_WIDTH) // TILE_SIZE) + 1

        positions = {f"{x}:{y}" for y in range(start_row, end_row + 1) for x in range(start_col, end_col + 1)}

        for layer in self.level:
            area[layer] = positions & self.tiles[layer]

        return area

    def draw_level(self, surf: pg.Surface, area: dict, cam_pos: pg.Vector2):
        for layer in area:
            for tile in area[layer]:
                x, y = map(int, tile.split(":"))
                tile_type = self.levels[self.current_level][layer][tile]["type"]
                tile_id = self.levels[self.current_level][layer][tile]["id"]
                if tile_type == "tiles":
                    tile_set = self.levels[self.current_level][layer][tile]["tile_set"]
                    surf.blit(self.types[tile_type][tile_set][tile_id], (x * TILE_SIZE - cam_pos.x, y * TILE_SIZE - cam_pos.y))
                else:
                    surf.blit(self.types[tile_type][tile_id], (x * TILE_SIZE - cam_pos.x, y * TILE_SIZE - cam_pos.y))


