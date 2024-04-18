import datetime
import pygame
from .computer import Computer
from .grid import Grid
from .inputs import Button
from .sql import (
    retrieve_settings_id,
    insert_settings,
    get_latest_settings_id,
    insert_game,
    get_latest_game_id,
    insert_move,
)
from .utils import Stack, format_time


class Game:
    return_button_x_offset = 0.03
    return_button_y_offset = 0.05
    return_button_w_prop = 0.18
    return_button_h_prop = 0.11

    title_font = pygame.font.SysFont("arial", 60, True)
    title_y_offset = 0.03

    cycle_button_x_offset = 0.1
    cycle_button_w_prop = 0.07
    cycle_button_h_prop = 0.05

    undo_button_x_offset = 0.1
    undo_button_y_offset = 0.85
    undo_button_w_prop = 0.15
    undo_button_h_prop = 0.11

    topologies = {
        "(0, 0)": "Plane",
        "(0, 1)": "Cylinder",
        "(0, -1)": "Mobius Strip",
        "(1, 1)": "Torus",
        "(1, -1)": "Klein Bottle",
        "(-1, -1)": "Projective Plane",
    }

    def __init__(self, w, h, settings, moves):
        self.w = w
        self.h = h
        self.is_interactive = True if not moves else False
        self.undo_enabled = settings[3]
        self.is_single_player = True if settings[6] == "Single-Player" else False

        self.return_button = Button(
            self.return_button_x_offset * self.w,
            self.return_button_y_offset * self.h,
            self.return_button_w_prop * self.w,
            self.return_button_h_prop * self.h,
            "Return",
        )

        self.current_player = 1
        self.outcome = 0

        if self.is_interactive:
            self.grid = Grid(*(settings[:3] + [settings[5]]))  # Composition
            if self.is_single_player:
                self.computer = Computer(self.grid, settings[4])  # Composition
        else:
            cycle_button_h = (0.5 - self.cycle_button_h_prop / 2) * self.h
            self.previous_button = Button(
                self.cycle_button_x_offset * self.w,
                cycle_button_h,
                self.cycle_button_w_prop * self.w,
                self.cycle_button_h_prop * self.h,
                "Previous",
                False,
                True,
            )
            self.next_button = Button(
                (1 - self.cycle_button_x_offset - self.cycle_button_w_prop) * self.w,
                cycle_button_h,
                self.cycle_button_w_prop * self.w,
                self.cycle_button_h_prop * self.h,
                "Next",
                False,
                True,
            )

            self.grid = Grid(
                *(settings[:3] + [settings[5]]), Stack(settings[1] ** 2, moves)
            )

        if self.undo_enabled and self.is_interactive:
            self.undo_button = Button(
                self.undo_button_x_offset * self.w,
                self.undo_button_y_offset * self.h,
                self.undo_button_w_prop * self.w,
                self.undo_button_h_prop * self.h,
                "Undo",
            )

        self.mouse_released = False

    def make_move(self, square):
        self.grid.move(square, self.current_player)
        outcome = self.grid.check_end(square, self.current_player)
        if outcome:
            self.outcome = outcome
            self.save_game()
        self.current_player = 3 - self.current_player

    def undo_move(self):
        if self.is_single_player:
            for _ in range(2):
                self.grid.previous_move(True)
        else:
            self.grid.previous_move(True)
            self.current_player = 3 - self.current_player

    def previous_move(self):
        self.grid.previous_move(False)
        self.outcome = 0
        self.current_player = 3 - self.current_player

    def next_move(self):
        self.grid.next_move(self.current_player)
        final_move = self.grid.moves.index(self.grid.current_move)
        if final_move == self.grid.moves.peek():
            self.outcome = self.grid.check_end(final_move, self.current_player)
        self.current_player = 3 - self.current_player

    def make_computer_move(self):
        square = self.computer.get_best_move()
        self.make_move(square)

    def save_game(self):
        # Settings Record
        topology = self.topologies[str(self.grid.topology)]
        settings_id = retrieve_settings_id(
            self.is_single_player,
            topology,
            self.grid.grid_size,
            self.grid.line_size,
        )
        if not settings_id:
            insert_settings(
                self.is_single_player,
                topology,
                self.grid.grid_size,
                self.grid.line_size,
            )
            settings_id = get_latest_settings_id()

        # Game Record
        now = datetime.datetime.now()
        if not self.outcome == 3:
            outcome = self.current_player
        else:
            outcome = 0
        insert_game(
            settings_id,
            outcome,
            now.day,
            now.month,
            now.year,
            format_time(now.hour, now.minute),
        )

        # Move Records
        move_no = 1
        game_id = get_latest_game_id()
        player = 1
        final_move = self.grid.moves.peek()
        while True:
            row, col = self.grid.moves.index(move_no - 1)
            insert_move(move_no, game_id, player, f"{row},{col}")
            if (row, col) == final_move:
                break
            move_no += 1
            player = 3 - player

    def loop_game(self, win, mouse_x, mouse_y, mouse_pressed):
        self.return_button.update(mouse_x, mouse_y, mouse_pressed)

        self.render(win)

        if not self.outcome:
            if self.undo_enabled:
                self.undo_button.update(mouse_x, mouse_y, mouse_pressed)
            grid_state = self.grid.get_state(win, mouse_x, mouse_y, mouse_pressed)

            if self.mouse_released:
                if grid_state and self.grid.grid[grid_state[0]][grid_state[1]] == 0:
                    self.make_move(grid_state)
                elif (
                    self.undo_enabled
                    and self.undo_button.state == 2
                    and (
                        self.is_single_player
                        and self.grid.current_move >= 1
                        or not self.is_single_player
                        and self.grid.current_move >= 0
                    )
                ):
                    self.undo_move()
                elif self.is_single_player and self.current_player == 2:
                    self.make_computer_move()

        elif self.mouse_released and self.return_button.state == 2:
            return "Return"

        if self.mouse_released == mouse_pressed:
            self.mouse_released = not mouse_pressed

    def loop_previous_game(self, win, mouse_x, mouse_y, mouse_pressed):
        self.return_button.update(mouse_x, mouse_y, mouse_pressed)
        self.previous_button.update(mouse_x, mouse_y, mouse_pressed)
        self.next_button.update(mouse_x, mouse_y, mouse_pressed)

        self.render(win)

        if self.mouse_released:
            if self.return_button.state == 2:
                return "Return"
            elif self.previous_button.state == 2 and not self.grid.current_move == -1:
                self.previous_move()
            elif self.next_button.state == 2 and not self.outcome:
                self.next_move()

        if self.mouse_released == mouse_pressed:
            self.mouse_released = not mouse_pressed

    def render(self, win):
        win.fill("white")

        self.grid.render(win)
        if not self.is_interactive or type(self.outcome) == list or self.outcome == 3:
            self.return_button.render(win)

        if type(self.outcome) == list:
            if self.current_player == 2:
                title_text = "Player 1 Won"
            else:
                title_text = (
                    "Computer" if self.is_single_player else "Player 2"
                ) + " Won"
            self.grid.render_line(win, self.outcome)

        elif self.outcome == 3:
            title_text = "Draw"

        elif self.current_player == 1:
            title_text = "Player 1's Turn"

        else:
            title_text = (
                "Computer's" if self.is_single_player else "Player 2's"
            ) + " Turn"

        title = self.title_font.render(title_text, True, "black")
        title_w = title.get_size()[0]
        win.blit(title, (self.w / 2 - title_w / 2, self.title_y_offset * self.h))

        if not self.is_interactive:
            if not self.grid.current_move == -1:
                self.previous_button.render(win)
            if not self.outcome:
                self.next_button.render(win)
        elif (
            self.undo_enabled and not self.grid.current_move == -1 and not self.outcome
        ):
            self.undo_button.render(win)
