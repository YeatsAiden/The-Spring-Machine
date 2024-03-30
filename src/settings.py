import pygame as pg
import json
import sys
import os
import math
import time

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 960, 480
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 256, 128

DIS_RATIO = min(WINDOW_WIDTH / DISPLAY_WIDTH, WINDOW_HEIGHT / DISPLAY_HEIGHT)

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
    "buttons": current_dir + "/assets/buttons",
    "objects": current_dir + "/assets/objects",
    "spawns": current_dir + "/assets/spawns",
}

