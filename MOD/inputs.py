import pygame
from .utils import point_in_rect

pygame.init()
pygame.font.init()


class Button:
    button_font = pygame.font.SysFont("arial", 50, True)
    small_button_font = pygame.font.SysFont("arial", 13)

    offset_x = 5
    offset_y = 5

    def __init__(self, x, y, w, h, text, selectable=False, is_small=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        if is_small:
            self.text = self.small_button_font.render(text, True, "black")
        else:
            self.text = self.button_font.render(text, True, "black")

        self.colour = (150, 150, 150)
        self.state = 0

        self.selected = False
        self.selectable = selectable
        if self.selectable:
            self.deselected = True

    def update(self, mouse_x, mouse_y, mouse_pressed):
        if (
            point_in_rect(mouse_x, mouse_y, self.x, self.y, self.w, self.h)
            and mouse_pressed
        ):
            self.state = 2
            if self.selectable and self.deselected:
                self.selected = bool(1 - int(self.selected))
                self.deselected = False
        else:
            self.state = 0
            if self.selectable and not self.deselected:
                self.deselected = True

    def render(self, win):
        if self.state == 2 or self.selected:
            colour = tuple([max(colour_comp - 50, 0) for colour_comp in self.colour])
        else:
            colour = self.colour

        pygame.draw.rect(win, colour, (self.x, self.y, self.w, self.h))
        win.blit(self.text, (self.x + self.offset_x, self.y + self.offset_y))


class ListOfButtons:
    offset = 5

    def __init__(self, x, y, w, h, button_count, texts, selected=None):
        self.buttons = []
        for i in range(button_count):
            self.buttons.append(Button(x, y, w, h, texts[i], False, True))
            x += self.buttons[-1].w + self.offset

        self.selected = selected
        if type(self.selected) == int:
            self.select(self.selected)

    def update(self, mouse_x, mouse_y, mouse_pressed):
        for i, button in enumerate(self.buttons):
            button.update(mouse_x, mouse_y, mouse_pressed)
            if button.state == 2:
                self.select(i)

    def select(self, index):
        if type(self.selected) == int:
            self.buttons[self.selected].selected = False
        self.buttons[index].selected = True
        self.selected = index

    def render(self, win):
        for button in self.buttons:
            button.render(win)


class CharInputBox:
    offset_x = 5
    offset_y = 5
    input_font = pygame.font.SysFont("arial", 30, True)

    def __init__(self, x, y, prompt, input_text):
        self.x = x
        self.y = y
        self.prompt = prompt
        self.prompt_w, self.prompt_h = self.prompt.get_size()
        self.input_text = input_text
        self.input = self.input_font.render(self.input_text, True, "black")
        input_w, input_h = self.input.get_size()
        self.w = self.prompt_w + input_w + self.offset_x * 4
        self.h = max(self.prompt_h, input_h) + self.offset_y * 2

    def check_selected(self, mouse_x, mouse_y, mouse_pressed):
        if (
            point_in_rect(mouse_x, mouse_y, self.x, self.y, self.w, self.h)
            and mouse_pressed
        ):
            return True

    def update_input(self, new_input_text):
        self.input_text = new_input_text
        self.input = self.input_font.render(self.input_text, True, "black")

    def render(self, win):
        pygame.draw.rect(win, "black", (self.x, self.y, self.w, self.h), 1)
        win.blit(self.prompt, (self.x + self.offset_x, self.y + self.offset_y))
        win.blit(
            self.input,
            (self.x + self.prompt_w + self.offset_x * 3, self.y + self.offset_y),
        )
        line_x = self.x + self.prompt_w + self.offset_x * 2
        pygame.draw.line(win, "black", (line_x, self.y), (line_x, self.y + self.h))
