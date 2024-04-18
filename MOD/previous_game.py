import math
import pygame
from .inputs import Button
from .sql import retrieve_previous_games, retrieve_win_rates, calculate_total_games


class PreviousGame:
    return_button_x_offset = 0.05
    return_button_y_offset = 0.05
    return_button_w_prop = 0.18
    return_button_h_prop = 0.11

    title = pygame.font.SysFont("arial", 50, True).render(
        "Load Previous Game", True, "black"
    )
    title_w = title.get_size()[0]
    title_y_offset = 0.05

    load_button_x_offset = 0.1
    load_button_y_offset = 0.18
    load_button_w_prop = 0.14
    load_button_h_prop = 0.11
    load_button_y_space = 0.03

    info_stats_font = pygame.font.SysFont("arial", 13)
    info_col1_x_offset = 0.03
    info_col2_x_offset = 0.3

    move_button_x_offset = 0.05
    move_button_y_offset = 0.87
    move_button_w_prop = 0.23
    move_button_h_prop = 0.11

    stats_font = pygame.font.SysFont("arial", 15)
    stats_y_offset = 0.87

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
        self.previous_button = Button(
            self.move_button_x_offset * self.w,
            self.move_button_y_offset * self.h,
            self.move_button_w_prop * self.w,
            self.move_button_h_prop * self.h,
            "Previous",
        )
        self.next_button = Button(
            (1 - self.move_button_x_offset - self.move_button_w_prop) * self.w,
            self.move_button_y_offset * self.h,
            self.move_button_w_prop * self.w,
            self.move_button_h_prop * self.h,
            "Next",
        )
        self.mouse_released = False

        self.total_games = calculate_total_games()
        self.player1_win_rate, self.player2_win_rate = retrieve_win_rates()

        self.page = 1
        self.previous_games_info = [{} for _ in range(5)]
        self.load_previous_games_info()

        self.load_buttons = []
        for count in range(5):
            self.load_buttons.append(
                Button(
                    self.load_button_x_offset * self.w,
                    (
                        self.load_button_y_offset
                        + (self.load_button_h_prop + self.load_button_y_space) * count
                    )
                    * self.h,
                    self.load_button_w_prop * self.w,
                    self.load_button_h_prop * self.h,
                    "Load",
                )
            )

    def load_previous_games_info(self):
        games_infos = retrieve_previous_games((self.page - 1) * 5)
        for i in range(5):
            if i < len(games_infos):
                game_info = games_infos[i]

                previous_game_info = self.previous_games_info[i]
                previous_game_info["Game ID"] = game_info[0]

                if game_info[2]:
                    previous_game_info["Game Mode"] = "Single-Player"
                else:
                    previous_game_info["Game Mode"] = "Multiplayer"

                if game_info[1] == 1:
                    previous_game_info["Game Outcome"] = "Player 1 Won"
                elif game_info[1] == 0:
                    previous_game_info["Game Outcome"] = "Draw"
                elif previous_game_info["Game Mode"] == "Single-Player":
                    previous_game_info["Game Outcome"] = "Computer Won"
                else:
                    previous_game_info["Game Outcome"] = "Player 2 Won"

                previous_game_info["Topology"] = game_info[3]
                previous_game_info["Grid Size"] = f"{game_info[4]}x{game_info[4]}"
                previous_game_info[
                    "Date"
                ] = f"{game_info[5]}/{game_info[6]}/{game_info[7]}"
                previous_game_info["Time"] = game_info[8]

            else:
                self.previous_games_info[i] = {}

    def next_page(self):
        self.page += 1
        self.load_previous_games_info()

    def previous_page(self):
        self.page -= 1
        self.load_previous_games_info()

    def loop(self, win, mouse_x, mouse_y, mouse_pressed):
        self.return_button.update(mouse_x, mouse_y, mouse_pressed)
        self.previous_button.update(mouse_x, mouse_y, mouse_pressed)
        self.next_button.update(mouse_x, mouse_y, mouse_pressed)

        for load_button in self.load_buttons:
            load_button.update(mouse_x, mouse_y, mouse_pressed)

        self.render(win)

        if self.mouse_released:
            if self.return_button.state == 2:
                return "Return"
            if self.previous_button.state == 2 and self.page > 1:
                self.previous_page()
            elif self.next_button.state == 2 and self.page < math.ceil(
                self.total_games / 5
            ):
                self.next_page()

            for i, load_button in enumerate(self.load_buttons):
                if load_button.state == 2 and self.previous_games_info[i] != {}:
                    return self.previous_games_info[i]["Game ID"]

        if self.mouse_released == mouse_pressed:
            self.mouse_released = not mouse_pressed

    def render_previous_game(self, win, num):
        load_button = self.load_buttons[num]
        previous_game_info = self.previous_games_info[num]

        load_button.render(win)

        y = (
            self.load_button_y_offset
            + (self.load_button_h_prop + self.load_button_y_space) * num
        ) * self.h

        info_col1 = [
            f"Game Outcome: {previous_game_info['Game Outcome']}",
            f"Game Mode: {previous_game_info['Game Mode']}",
            f"Topology: {previous_game_info['Topology']}",
            f"Grid Size: {previous_game_info['Grid Size']}",
        ]
        y_offset = 0
        for info_col1_line in info_col1:
            info_col1_rendered_line = self.info_stats_font.render(
                info_col1_line, True, "black"
            )
            win.blit(
                info_col1_rendered_line,
                (
                    (
                        self.load_button_x_offset
                        + self.load_button_w_prop
                        + self.info_col1_x_offset
                    )
                    * self.w,
                    y + y_offset,
                ),
            )
            y_offset += info_col1_rendered_line.get_size()[1]

        info_col2 = [
            f"Date: {previous_game_info['Date']}",
            f"Time: {previous_game_info['Time']}",
        ]
        y_offset = 0
        for info_col2_line in info_col2:
            info_col2_rendered_line = self.info_stats_font.render(
                info_col2_line, True, "black"
            )
            win.blit(
                info_col2_rendered_line,
                (
                    (
                        self.load_button_x_offset
                        + self.load_button_w_prop
                        + self.info_col2_x_offset
                    )
                    * self.w,
                    y + y_offset,
                ),
            )
            y_offset += info_col2_rendered_line.get_size()[1]

    def render(self, win):
        win.fill("white")

        self.return_button.render(win)

        win.blit(
            self.title,
            (self.w / 2 - self.title_w / 2, self.title_y_offset * self.h),
        )

        for i in range(5):
            if self.previous_games_info[i]:
                self.render_previous_game(win, i)

        self.previous_button.render(win)
        self.next_button.render(win)

        stats_text = [
            f"Total Games: {self.total_games}",
            f"Player 1 Win Rate: {round(self.player1_win_rate * 100, 1)}%",
            f"Player 2 / Computer Win Rate: {round(self.player2_win_rate * 100, 1)}%",
        ]
        y_offset = 0
        for stats_text_line in stats_text:
            stats_line = self.stats_font.render(stats_text_line, True, "black")
            stats_line_w, stats_line_h = stats_line.get_size()
            win.blit(
                stats_line,
                (
                    self.w / 2 - stats_line_w / 2,
                    self.stats_y_offset * self.h + y_offset,
                ),
            )
            y_offset += stats_line_h
