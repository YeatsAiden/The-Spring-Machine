from settings import *
from ui import Button, Font
from level import *

# Initial setup
pg.init()

window = pg.display.set_mode(WINDOW_SIZE, FLAGS)
display = pg.Surface(DISPLAY_SIZE)
clock = pg.time.Clock()
pg.mouse.set_visible(MOUSE_VISIBLE)

# Loading assets
objects = load_images(PATHS["objects"])
spawns = load_images(PATHS["spawns"])
tile_sets = {file.split('.')[0]: make_tileset_dict(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "png"}
tile_sets_rules = {file.split('.')[0]: load_json(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "json"}

# Class initialization
smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)

# Display stuff
cam_pos = pg.Vector2(0, 0)
xy_change = [0, 0]
scale = 1

# Game loop
while True:
    display.fill("black")

    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed()

    current_time = time.time()

    cam_pos.x += ( - cam_pos.x)/5
    cam_pos.y += ( - cam_pos.y)/5

    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_x = (mouse_x - xy_change[0])/scale
    mouse_y = (mouse_y - xy_change[1])/scale

    # event_loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F11:
                FULL_SCREEN = not FULL_SCREEN
                pg.display.set_mode((0, 0), FLAGS | pg.FULLSCREEN) if FULL_SCREEN else pg.display.set_mode(WINDOW_SIZE, FLAGS) 

    # Resizing display to window size
    display_cp, xy_change, scale = resize_surface(window, display)
    window.blit(display_cp, xy_change)

    pg.display.update()
    dt = clock.tick(FPS) / 1000