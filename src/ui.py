from typing import Any
from settings import *
from core_funcs import *


class Button:
    def __init__(self, image: str | pg.Surface, x: int = 0, y: int = 0) -> None:
        if isinstance(image, str):
            self.button_img = pg.image.load(image).convert_alpha()
        else:
            self.button_img = image

        self.rect = self.button_img.get_rect()
        self.rect.topleft = [x, y]

        self.click_cooldown = 1
        self.time_since_click = 0
        
    
    def check_click(self, mouse_pos, mouse_pressed, current_time):
        click = False

        # check mouseover and clicked conditions
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0] and (current_time - self.time_since_click) > self.click_cooldown:
            self.time_since_click = time.time()
            click = True
        # return if clicked
        return click
    
    def set_position(self, x: int, y: int):
        self.rect.topleft = [x, y]

    def draw(self, surf: pg.Surface):
        surf.blit(self.button_img, (self.rect.x, self.rect.y))

        
class Font:
    def __init__(self, path: str, include: list[int, int, int], step: int) -> None:
        self.characters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789", "!@#$%^&*()`~-_=+\\|[]}{';:/?.>,<"]

        self.font = self.load_font(path, include, step)
    
    def load_font(self, path: str, include: list[int, int, int], step: int):
        font_img = pg.image.load(path).convert()
        font_img.set_colorkey((0, 0, 0))
        
        characters = []
        font = {}

        x_pos = 0

        for x in range(font_img.get_width()):
            for y in range(font_img.get_height()):
                color = font_img.get_at((x, y))

                if color == (255, 0, 0, 255):
                    character = clip_img(font_img, x_pos, 0, x - x_pos, font_img.get_height())
                    x_pos = x + 1

                    if y == 1:
                        cp_surface = character.copy()
                        character = pg.Surface((cp_surface.get_width(), cp_surface.get_height() + step))
                        character.blit(cp_surface, (0, step))
                    characters.append(character)
        
        for i in include:
            for character in self.characters[i]:
                font[character] = characters[len(font)]
        
        return font
    
    def draw_text(self, surface: pg.Surface, text: str, x: int, y: int, space: int, size: int):
        x_pos = 0
        for letter in text:
            if letter == " ":
                x_pos += space * size
            else:
                character_img = pg.transform.scale_by(self.font[letter], size)
                surface.blit(character_img, (x + x_pos, y))
                x_pos += character_img.get_width() + size
