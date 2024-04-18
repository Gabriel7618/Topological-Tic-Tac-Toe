import pygame
from .inputs import Button

pygame.init()
pygame.font.init()


class Menu:
    title = pygame.font.SysFont("arial", 75, True).render("Menu", True, "black")
    title_w = title.get_size()[0]
    title_offset = 0.05

    button_w_prop = 0.6
    button_h_prop = 0.17
    button_top_offset = 0.3
    button_y_offset = 0.05

    def __init__(self, w, h):
        self.w = w
        self.h = h

        button_x = self.w / 2 - self.button_w_prop * self.w / 2
        button_w = self.button_w_prop * self.w
        button_h = self.button_h_prop * self.h

        self.settings_button = Button(
            button_x,
            self.button_top_offset * self.h,
            button_w,
            button_h,
            "Settings",
        )
        self.game_button = Button(
            button_x,
            self.settings_button.y
            + self.settings_button.h
            + self.button_y_offset * self.h,
            button_w,
            button_h,
            "Play Game",
        )
        self.previous_game_button = Button(
            button_x,
            self.game_button.y + self.game_button.h + self.button_y_offset * self.h,
            button_w,
            button_h,
            "Load Previous Game",
        )

        self.mouse_released = False

    def loop(self, win, mouse_x, mouse_y, mouse_pressed):
        self.settings_button.update(mouse_x, mouse_y, mouse_pressed)
        self.game_button.update(mouse_x, mouse_y, mouse_pressed)
        self.previous_game_button.update(mouse_x, mouse_y, mouse_pressed)

        self.render(win)

        if self.mouse_released:
            if self.settings_button.state == 2:
                return "Settings"
            if self.game_button.state == 2:
                return "Play Game"
            if self.previous_game_button.state == 2:
                return "Previous Game"

        if self.mouse_released == mouse_pressed:
            self.mouse_released = not mouse_pressed

    def render(self, win):
        win.fill("white")
        win.blit(
            self.title, (self.w / 2 - self.title_w / 2, self.title_offset * self.h)
        )
        self.settings_button.render(win)
        self.game_button.render(win)
        self.previous_game_button.render(win)
