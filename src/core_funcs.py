from settings import *


def clip_img(surf, x: int, y: int, width: int, height: int):
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())


def get_file_names(dir_path: str):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            files.append(path.split("/")[-1])
    return files


def get_dir_names(dir_path: str):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, path)):
            files.append(path)
    return sorted(files)


def load_images(path: str):
    img_names = get_file_names(path)
    images = {}

    for name in img_names:
        img_path = path + "/" + name
        img = pg.image.load(img_path).convert_alpha()
        img.set_colorkey((0, 0, 0))
        images[name.split(".")[0]] = img

    return images


def make_tileset_dict(tileset_path: str):
    tileset = {}
    tileset_img = pg.image.load(tileset_path).convert_alpha()
    for y in range(0, tileset_img.get_height(), TILE_SIZE):
        for x in range(0, tileset_img.get_width(), TILE_SIZE):
            img = clip_img(tileset_img, x, y, TILE_SIZE, TILE_SIZE)

            if check_if_sprite_is_not_transparent(img):
                tileset[y//TILE_SIZE * tileset_img.get_width()//TILE_SIZE + x//TILE_SIZE] = img
    
    return tileset


def check_if_sprite_is_not_transparent(surf: pg.Surface):
    for y in range(0, surf.get_height()):
        for x in range(0, surf.get_width()):
            if surf.get_at((x, y))[3] > 0:
                return True
    return False


def resize_surface(parent_surf : pg.Surface, child_surf : pg.Surface):
    # Checks how the display should scale depending on the window size.
    width_ratio = parent_surf.get_width() / child_surf.get_width()
    height_ratio = parent_surf.get_height() / child_surf.get_height()

    scale = min(width_ratio, height_ratio)
    # Changes child_surf size to a new size using scale variable.
    surf = pg.transform.scale(child_surf, (scale * child_surf.get_width(), scale * child_surf.get_height()))
    # This returns the values for centering the scalled surface
    xy_change = [(parent_surf.get_width() - surf.get_width()) // 2, (parent_surf.get_height() - surf.get_height()) // 2]

    return surf, xy_change, scale


def load_json(path: str):
    with open(path) as f:
        json_data = json.load(f)
    return json_data


def timer(current_time, prev_time, cool_down):
    return current_time - prev_time >= cool_down


def freeze_frame(condition: bool, freeze: bool, freeze_duration: int, time_since_freeze: float, current_time: float):
    if condition and not freeze:
        freeze = True
        time_since_freeze = time.time()
    if freeze and timer(current_time, time_since_freeze, freeze_duration):
        freeze = False
        return freeze, time_since_freeze, True

    return freeze, time_since_freeze, False


def get_display_mouse_pos(scale, xy_change):
    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_x = (mouse_x - xy_change[0]) / scale
    mouse_y = (mouse_y - xy_change[1]) / scale

    return mouse_x, mouse_y


def load_sound(path: str):
    return pg.mixer.Sound(path)