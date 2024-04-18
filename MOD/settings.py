import pygame
from .inputs import Button, ListOfButtons, CharInputBox


class Settings:
    return_button_x_offset = 0.05
    return_button_y_offset = 0.05
    return_button_w_prop = 0.18
    return_button_h_prop = 0.11

    title = pygame.font.SysFont("arial", 75, True).render("Settings", True, "black")
    title_w = title.get_size()[0]
    title_y_offset = 0.05

    error_msg_font = pygame.font.SysFont("arial", 18)
    error_msg_x_offset = 0.7
    error_msg_y_offset = 0.05
    error_msg_w_prop = 0.25
    error_msg_h_prop = 0.15

    input_x_offset = 0.1
    input_x_spacing = 0.05
    input_y_spacing = 0.04

    topology_prompt = pygame.font.SysFont("arial", 15, True).render(
        "Select Topology", True, "black"
    )
    topology_prompt_w, topology_prompt_h = topology_prompt.get_size()

    topology_buttons_y_offset = 0.25
    topology_button_w_prop = 0.11
    topology_button_h_prop = 0.05

    grid_size_prompt = pygame.font.SysFont("arial", 15, True).render(
        "Side Length of Square Grid", True, "black"
    )

    line_size_prompt = pygame.font.SysFont("arial", 15, True).render(
        "Length of Line Needed to Win", True, "black"
    )

    undo_button_w_prop = 0.09
    undo_button_h_prop = 0.05

    moves_prompt = pygame.font.SysFont("arial", 10, True).render(
        "Number of Moves Computer can Foresee Ahead", True, "black"
    )

    adjacency_map_button_w_prop = 0.15
    adjacency_map_button_h_prop = 0.05

    game_mode_prompt = pygame.font.SysFont("arial", 20, True).render(
        "Game Mode", True, "black"
    )
    game_mode_prompt_x, game_mode_prompt_h = game_mode_prompt.get_size()

    game_mode_button_w_prop = 0.09
    game_mode_button_h_prop = 0.05

    topologies = ((0, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1))
    game_modes = ("Single-Player", "Multiplayer")

    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.return_button = Button(
            self.return_button_x_offset * self.w,
            self.return_button_y_offset * self.h,
            self.return_button_w_prop * self.w,
            self.return_button_h_prop * self.h,
            "Return",
        )

        x = self.input_x_offset * self.w
        self.topology_buttons = ListOfButtons(
            x + self.topology_prompt_w + self.input_x_spacing * self.w,
            self.topology_buttons_y_offset * self.h,
            self.topology_button_w_prop * self.w,
            self.topology_button_h_prop * self.h,
            6,
            [
                "Plane",
                "Cylinder",
                "Mobius Strip",
                "Torus",
                "Klein Bottle",
                "Projective Plane",
            ],
            0,
        )
        self.grid_size_inp = CharInputBox(
            x,
            (
                self.topology_buttons_y_offset
                + self.topology_button_h_prop
                + self.input_y_spacing
            )
            * self.h,
            self.grid_size_prompt,
            "3",
        )
        self.line_size_inp = CharInputBox(
            x,
            self.grid_size_inp.y + self.grid_size_inp.h + self.input_y_spacing * self.h,
            self.line_size_prompt,
            "3",
        )
        self.undo_button = Button(
            x,
            self.line_size_inp.y + self.line_size_inp.h + self.input_y_spacing * self.h,
            self.undo_button_w_prop * self.w,
            self.undo_button_h_prop * self.h,
            "Enable Undo",
            True,
            True,
        )
        self.moves_inp = CharInputBox(
            x,
            self.undo_button.y + self.undo_button.h + self.input_y_spacing * self.h,
            self.moves_prompt,
            "3",
        )
        self.adjacency_map_button = Button(
            x,
            self.moves_inp.y + self.moves_inp.h + self.input_y_spacing * self.h,
            self.adjacency_map_button_w_prop * self.w,
            self.adjacency_map_button_h_prop * self.h,
            "Display Adjacency Map",
            True,
            True,
        )
        self.game_mode_buttons = ListOfButtons(
            x + self.game_mode_prompt_x + self.input_x_spacing * self.w,
            self.adjacency_map_button.y
            + self.adjacency_map_button.h
            + self.input_y_spacing * self.h,
            self.game_mode_button_w_prop * self.w,
            self.game_mode_button_h_prop * self.h,
            2,
            ["Single Player", "Multi-Player"],
            0,
        )
        self.mouse_released = False

        self.error_msg = None

    def validate_inputs(self):
        grid_size = int(self.grid_size_inp.input_text)
        line_size = int(self.line_size_inp.input_text)
        moves = int(self.moves_inp.input_text)

        if grid_size not in (3, 4, 5, 6):
            self.error_msg = "Side Length of Square\nGrid must be 3, 4, 5 or 6"
        elif not line_size > 0:
            self.error_msg = "Length of Line Needed\nto Win must be greater than 0"
        elif not line_size <= grid_size:
            self.error_msg = "Length of Line Needed to\nWin cannot be greater than\nSide Length of Square Grid"
        elif not moves > 0:
            self.error_msg = (
                "Number of Moves\nComputer can Foresee\nAhead must be greater\nthan 0"
            )
        elif not moves <= 5:
            self.error_msg = (
                "Number of Moves\nComputer can Foresee\nAhead cannot be more\nthan 5"
            )
        else:
            self.error_msg = ""

    def loop(self, win, mouse_x, mouse_y, mouse_pressed):
        self.return_button.update(mouse_x, mouse_y, mouse_pressed)
        self.topology_buttons.update(mouse_x, mouse_y, mouse_pressed)
        self.undo_button.update(mouse_x, mouse_y, mouse_pressed)
        self.adjacency_map_button.update(mouse_x, mouse_y, mouse_pressed)
        self.game_mode_buttons.update(mouse_x, mouse_y, mouse_pressed)

        self.validate_inputs()

        self.render(win)

        if self.mouse_released:
            if self.grid_size_inp.check_selected(mouse_x, mouse_y, mouse_pressed):
                return "Grid Size Input"
            if self.line_size_inp.check_selected(mouse_x, mouse_y, mouse_pressed):
                return "Line Size Input"
            if self.moves_inp.check_selected(mouse_x, mouse_y, mouse_pressed):
                return "Moves Input"
            if not self.error_msg and self.return_button.state == 2:
                return [
                    self.topologies[self.topology_buttons.selected],
                    int(self.grid_size_inp.input_text),
                    int(self.line_size_inp.input_text),
                    self.undo_button.selected,
                    int(self.moves_inp.input_text),
                    self.adjacency_map_button.selected,
                    self.game_modes[self.game_mode_buttons.selected],
                ]

        if self.mouse_released == mouse_pressed:
            self.mouse_released = not mouse_pressed

    def render_error(self, win):
        pygame.draw.rect(
            win,
            "red",
            (
                self.error_msg_x_offset * self.w,
                self.error_msg_y_offset * self.h,
                self.error_msg_w_prop * self.w,
                self.error_msg_h_prop * self.h,
            ),
        )

        error_msg_lines = self.error_msg.split("\n")
        y_offset = 3
        for error_msg_line in error_msg_lines:
            error_line = self.error_msg_font.render(error_msg_line, True, "black")
            error_line_w, error_line_h = error_line.get_size()
            win.blit(
                error_line,
                (
                    (self.error_msg_x_offset + self.error_msg_w_prop / 2) * self.w
                    - error_line_w / 2,
                    self.error_msg_y_offset * self.h + y_offset,
                ),
            )
            y_offset += error_line_h

    def render(self, win):
        win.fill("white")

        self.return_button.render(win)
        win.blit(
            self.title,
            (self.w / 2 - self.title_w / 2, self.title_y_offset * self.h),
        )
        if self.error_msg:
            self.render_error(win)

        win.blit(
            self.topology_prompt,
            (self.input_x_offset * self.w, self.topology_buttons_y_offset * self.h),
        )
        win.blit(
            self.game_mode_prompt,
            (self.input_x_offset * self.w, self.game_mode_buttons.buttons[0].y),
        )

        self.topology_buttons.render(win)
        self.grid_size_inp.render(win)
        self.line_size_inp.render(win)
        self.undo_button.render(win)
        self.moves_inp.render(win)
        self.adjacency_map_button.render(win)
        self.game_mode_buttons.render(win)
