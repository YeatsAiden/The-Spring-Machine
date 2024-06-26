import pygame as pg
import json
import sys
import os
import math
import time
import random

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 960, 480
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 192

FLAGS = pg.RESIZABLE

FULL_SCREEN = False

TILE_SIZE = 16

FPS = 60

MOUSE_VISIBLE = False

current_dir = os.getcwd()
PATHS = {
    "tilesets": current_dir + "/assets/tilesets",
    "levels": current_dir + "/assets/levels",
    "fonts": current_dir + "/assets/fonts",
    "buttons": current_dir + "/assets/ui/buttons",
    "objects": current_dir + "/assets/objects",
    "spawns": current_dir + "/assets/spawns",
    "player": current_dir + "/assets/player",
    "cursor": current_dir + "/assets/ui/cursor.png",  # i dont know what im doing, okay?? - Andrey | ok ._. - Aiden
    "music": current_dir + "/assets/music",
    "enemies": current_dir + "/assets/enemies",
    "flowey": current_dir + "/assets/enemies/flowey",
    "glacierd": current_dir + "/assets/enemies/glacierd",
    "angle": current_dir + "/assets/enemies",
    "particle": current_dir + "/assets/particles",
    "backgrounds": current_dir + "/assets/background",
    "fire-ring": current_dir + "/assets/other/fire-ring.png",
    "sound": current_dir + "/assets/sounds",
}

