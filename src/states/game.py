try:
    from settings import *
    from ui import *
    from level import Level
    from player import Player
    from enemies.glacierd import Glacierd
    from enemies.flowey import Flowey
    from enemies.angle import Angel
    from enemies.angle_bomb import AngelBomb
    from enemies.flowey_spore import FloweySpore
except:
    from src.settings import *
    from src.ui import *
    from src.level import Level
    from src.player import Player
    from src.enemies.glacierd import Glacierd
    from src.enemies.flowey import Flowey
    from src.enemies.angle import Angel
    from src.enemies.angle_bomb import AngelBomb
    from src.enemies.flowey_spore import FloweySpore

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
        self.current_level = self.levels["0"]

        self.load_entity_position_from_level_data(self.current_level)

        self.tile_area: dict[str, dict[str, pg.Rect | pg.FRect]]
        self.rect_area: dict[str, dict[str, pg.Rect | pg.FRect]]

        self.cam_pos = pg.Vector2(0, 0)

        self.music_playing = random.choice(["melting-through", "breaking-ice"])
    

    def update(self, *args):
        dt = args[0]
        current_time = args[1]
        keys_pressed = args[3]
        sound_manager = args[4]

        sound_manager.play_music(self.music_playing, 0.5)

        self.cam_pos.x += (self.player.rect.x - self.cam_pos.x - DISPLAY_WIDTH/2)/10
        self.cam_pos.y += (self.player.rect.y - self.cam_pos.y - DISPLAY_HEIGHT/2)/10


        self.tile_area = self.levels["0"].get_area(self.cam_pos)
        self.rect_area = self.levels["0"].get_rects(self.tile_area)

        self.player.move(keys_pressed, dt, self.rect_area, current_time)

        self.update_entities(self.floweys, self.glacierds, self.angles, self.angle_bombs, self.flowey_spores, self.player.rect.center, current_time, dt, self.rect_area, self.cam_pos)

    def draw(self, *args):
        surf = args[0]
        current_time = args[1]
        mega_cool_art = args[2]

        surf.blit(mega_cool_art, (0, 0))
        self.levels["0"].draw_level(surf, self.tile_area, self.cam_pos)

        self.draw_entities(self.floweys, self.glacierds, self.angles, self.angle_bombs, self.flowey_spores, surf, self.cam_pos, current_time)

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

    def update_entities(self,
                        floweys: list[Flowey],
                        glacierds: list[Glacierd],
                        angles: list[Angel],
                        angle_bombs: list[AngelBomb],
                        flowey_spores: list[FloweySpore],
                        player_pos,
                        current_time,
                        dt,
                        rects,
                        cam_pos):

        for flowey in floweys:
            flowey.update(player_pos, current_time, self.check_entity_in_bounds(cam_pos, flowey))

            if flowey.time_to_spit_spore:
                flowey_spores.append(FloweySpore(PATHS["enemies"], flowey.rect.center, current_time))

        for glacierd in glacierds:
            glacierd.move(dt, rects, current_time, self.check_entity_in_bounds(cam_pos, glacierd), player_pos)

        for angle in angles:
            angle.move(dt, rects, current_time, self.check_entity_in_bounds(cam_pos, angle), player_pos)

            if angle.time_to_spawn_a_bomb and self.check_entity_in_bounds(cam_pos, angle):
                angle_bombs.append(AngelBomb(PATHS["enemies"], angle.rect.center))

        # angle bombs special stuff
        angle_bombs_to_exterminate = []
        for i, angle_bomb in enumerate(angle_bombs):
            angle_bomb.move(dt, rects, current_time, self.check_entity_in_bounds(cam_pos, angle_bomb))
            if angle_bomb.state == "done exploding":
                angle_bombs_to_exterminate.append(i)

        for i in angle_bombs_to_exterminate[::-1]:  # hard to explain why reverse, but it is required
            angle_bombs.pop(i)

        # flowey spores special stuff
        spores_to_eliminate = []
        for i, spore in enumerate(flowey_spores):
            spore.move(dt, rects, current_time, self.check_entity_in_bounds(cam_pos, spore), player_pos)

            if spore.state == "not existing":
                spores_to_eliminate.append(i)

        for i in spores_to_eliminate[::-1]:
            flowey_spores.pop(i)

    def draw_entities(self, floweys, glacierds, angles, angle_bombs, flowey_spores, surf, cam_pos, current_time):
        for flowey in floweys:
            flowey.draw(surf, cam_pos)

        for glacierd in glacierds:
            glacierd.draw(surf, cam_pos, current_time)

        for angle in angles:
            angle.draw(surf, cam_pos, current_time)

        for angle_bomb in angle_bombs:
            angle_bomb.draw(surf, cam_pos, current_time)

        for spore in flowey_spores:
            spore.draw(surf, cam_pos, current_time)

    def check_entity_in_bounds(self, cam_pos, entity):
        if not (cam_pos.y < (entity.rect.y + entity.rect.h) and entity.rect.y < (cam_pos.y + DISPLAY_HEIGHT)):
            return False

        if not (cam_pos.x < (entity.rect.x + entity.rect.w) and entity.rect.x < (cam_pos.x + DISPLAY_WIDTH)):
            return False

        return True

    def load_entity_position_from_level_data(self, level_data):
        self.glacierds = []
        self.floweys = []
        self.angles = []
        self.angle_bombs = []
        self.flowey_spores = []

        entities = {"flowey": (Flowey, self.floweys),
                    "glacierd": (Glacierd, self.glacierds),
                    "angle": (Angel, self.angles)}

        for _, spawns in level_data.spawns.items():
            for pos, spawn in spawns.items():
                pos = list(map(int, pos.split(":")))
                pos[0] *= TILE_SIZE
                pos[1] *= TILE_SIZE
                spawn = spawn.split("_")[0]

                if spawn == "player":
                    self.player = Player(PATHS["player"], pos)
                else:
                    entities[spawn][1].append(entities[spawn][0](PATHS[spawn], pos))


