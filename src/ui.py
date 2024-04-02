from typing import Any
from settings import *
from core_funcs import *
from animation import Animation

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


class Button:
    def __init__(self,
                 still: pg.Surface | Animation,  # what to draw if the button is left alone
                 hover: pg.Surface | Animation,  # what to draw if you hover over the button      DUH
                 click: pg.Surface | Animation,  # what to draw if you click on the button
                 rect: pg.Rect,
                 text: str = None,
                 text_pos: tuple[int, int] = (0, 0),
                 text_size: int = 1,
                 text_space: int = 1) -> None:

        self.rect = rect

        self.still, self.hover, self.click = still, hover, click

        self.text = text
        self.text_pos = text_pos
        self.text_size = text_size
        self.text_space = text_space

        self.pressed = False  # needed for knowing what type of image/animation to draw
        self.hovered = False

        self.click_cooldown = 1
        self.time_since_click = 0

    def check_click(self, mouse_pos, mouse_pressed, current_time):
        click = False

        # check mouseover and clicked conditions
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0] and (current_time - self.time_since_click) > self.click_cooldown:
            self.time_since_click = current_time
            click = True
        # return if clicked
        return click

    def check_hover(self, mouse_pos):
        hover = False

        if self.rect.collidepoint(mouse_pos):
            hover = True

        return hover

    def set_position(self, x: int, y: int):
        self.rect.topleft = x, y

    def draw_state(self, surf, state, font: Font):
        if isinstance(state, pg.Surface):
            image = state
        else:
            image = state.animate(False)

        if self.text is not None:
            font.draw_text(image, self.text, self.text_pos[0], self.text_pos[1], self.text_space, self.text_size)

        surf.blit(image, self.rect)

    def draw(self, surf: pg.Surface, font: Font):
        if self.pressed:
            self.draw_state(surf, self.click, font)
        elif self.hovered:
            self.draw_state(surf, self.hover, font)
        else:
            self.draw_state(surf, self.still, font)

    def update(self, mouse_pos, mouse_pressed, current_time):
        self.pressed = self.check_click(mouse_pos, mouse_pressed, current_time)
        self.hovered = self.check_hover(mouse_pos)

        if not self.pressed and isinstance(self.click, Animation):
            self.click.reset()

        if not self.hovered and isinstance(self.hover, Animation):
            self.hover.reset()

        if self.pressed or self.hovered:
            if isinstance(self.still, Animation):
                self.still.reset()
