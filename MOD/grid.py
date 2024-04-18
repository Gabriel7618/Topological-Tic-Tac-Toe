import pygame
from .utils import Stack


class Grid:  # Programming to interface
    grid_length = 250
    vect_to_string = {
        "(-1, -1)": "db",
        "(-1, 0)": "v",
        "(-1, 1)": "df",
        "(0, -1)": "h",
        "(0, 1)": "h",
        "(1, -1)": "df",
        "(1, 0)": "v",
        "(1, 1)": "db",
    }  # Dictionary

    def __init__(
        self,
        topology,
        grid_size,
        line_size,
        is_adjacency_map,
        moves=None,
    ):
        self.topology = topology
        self.grid_size = grid_size
        self.grid = [
            [0 for _ in range(self.grid_size + 2)] for _ in range(self.grid_size + 2)
        ]  # Multi-dimensional array
        self.line_size = line_size
        self.is_adjacency_map = is_adjacency_map

        self.moves = moves
        if not self.moves:
            self.moves = Stack(self.grid_size**2)  # Stack Operations
        self.current_move = -1

    def get_state(self, win, mouse_x, mouse_y, mouse_pressed):
        if mouse_pressed:
            width, height = win.get_size()

            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if (
                        height / 2
                        - self.grid_length / 2
                        + self.grid_length / self.grid_size * row
                        < mouse_y
                        < height / 2
                        - self.grid_length / 2
                        + self.grid_length / self.grid_size * (row + 1)
                        and width / 2
                        - self.grid_length / 2
                        + self.grid_length / self.grid_size * col
                        < mouse_x
                        < width / 2
                        - self.grid_length / 2
                        + self.grid_length / self.grid_size * (col + 1)
                    ):
                        return (row + 1, col + 1)
        return 0

    def update_grid(self, square, value):
        self.grid[square[0]][square[1]] = value

        if self.is_adjacency_map:
            for r, row in enumerate(self.grid):
                for c, col in enumerate(row):
                    if r in (0, self.grid_size + 1) or c in (0, self.grid_size + 1):
                        corr = self.corr_square([r, c])
                        if corr == square:
                            self.grid[r][c] = value

    def corr_square(self, square):  # Complex Mathematical Model
        corr = square[:]
        for dimension in range(2):
            if self.topology[dimension] != 0 and (
                corr[dimension] == 0 or corr[dimension] == self.grid_size + 1
            ):
                if corr[dimension] == 0:
                    corr[dimension] = self.grid_size
                else:
                    corr[dimension] = 1

                if self.topology[dimension] == -1:
                    other = 0**dimension
                    corr[other] = self.grid_size + 1 - corr[other]

        return tuple(corr)

    def adj_square(self, square, direction):
        adjacent = [0, 0]
        for index in range(2):
            adjacent[index] = square[index] + direction[index]
        return self.corr_square(adjacent)

    def move(self, square, player):
        self.update_grid(square, player)
        self.moves.push(square)  # Stack Operations
        self.current_move += 1

    def previous_move(self, is_interactive):
        if is_interactive:
            move = self.moves.pop()  # Stack Operations
        else:
            move = self.moves.index(self.current_move)
        self.update_grid(move, 0)
        self.current_move -= 1

    def next_move(self, player):
        self.current_move += 1
        move = self.moves.index(self.current_move)
        self.update_grid(move, player)

    def check_end(self, square, player):  # Programming to interface
        outcome = self.check_line(square, player)
        if outcome:
            return outcome
        elif self.moves.full():  # Stack Operations
            return 3
        else:
            return False

    def add_squares(
        self, square, dir_row, dir_col, line, player
    ):  # Complex user-defined algorithm
        row, col = square

        for _ in range(self.line_size - len(line)):
            new_row, new_col = self.adj_square([row, col], (dir_row, dir_col))
            new_dir_row, new_dir_col = dir_row, dir_col

            if self.topology[0] == -1 and (
                row == 1 and dir_row == -1 or row == self.grid_size and dir_row == 1
            ):
                new_dir_col *= -1
            if self.topology[1] == -1 and (
                col == 1 and dir_col == -1 or col == self.grid_size and dir_col == 1
            ):
                new_dir_row *= -1

            if row == new_row and col == new_col:
                break

            row, col = new_row, new_col
            dir_row, dir_col = new_dir_row, new_dir_col
            if row < 1 or row > self.grid_size or col < 1 or col > self.grid_size:
                break
            elif self.grid[row][col] != player:
                break
            else:
                line.append((row, col))

        return line

    def check_line(self, square, player):
        line = [square]

        for dir_row in range(-1, 1):
            for dir_col in range(-1, 2):
                if dir_row == dir_col == 0:
                    break

                line = self.add_squares(square, dir_row, dir_col, line, player)
                line = self.add_squares(square, -dir_row, -dir_col, line, player)
                if len(line) == self.line_size:
                    return line
                line = [square]

        return False

    def get_orientations(self, line):  # Complex user-defined algorithm
        if len(line) == 1:
            return {str(line[0]): "h"}

        line_orientations = {}
        for dir_row in range(-1, 2):
            for dir_col in range(-1, 2):
                if dir_row == dir_col == 0:
                    continue

                next_square = line[0]
                for square_num in range(len(line)):
                    if square_num == 1:
                        line_orientations[str((row, col))] = self.vect_to_string[
                            str((dir_row, dir_col))
                        ]

                    new_dir_row, new_dir_col = dir_row, dir_col

                    if square_num != 0:
                        if self.topology[0] == -1 and (
                            row == 1
                            and dir_row == -1
                            or row == self.grid_size
                            and dir_row == 1
                        ):
                            new_dir_col *= -1
                        if self.topology[1] == -1 and (
                            col == 1
                            and dir_col == -1
                            or col == self.grid_size
                            and dir_col == 1
                        ):
                            new_dir_row *= -1

                    row, col = next_square
                    dir_row, dir_col = new_dir_row, new_dir_col
                    if square_num > 0:
                        line_orientations[str((row, col))] = self.vect_to_string[
                            str((dir_row, dir_col))
                        ]

                    next_square = self.corr_square([row + dir_row, col + dir_col])
                    if next_square not in line:
                        break

        return line_orientations

    def render_line(self, win, line):
        win_width, win_height = win.get_size()
        square_length = self.grid_length / self.grid_size
        left_x = win_width / 2 - self.grid_length / 2
        top_y = win_height / 2 - self.grid_length / 2

        line_orientations = self.get_orientations(line)

        for square in line:
            if line_orientations[str(square)] == "h":
                y = top_y + (square[0] - 0.5) * square_length
                start_point = (left_x + (square[1] - 1) * square_length, y)
                end_point = (left_x + square[1] * square_length, y)
            elif line_orientations[str(square)] == "v":
                x = left_x + (square[1] - 0.5) * square_length
                start_point = (x, top_y + (square[0] - 1) * square_length)
                end_point = (x, top_y + square[0] * square_length)
            elif line_orientations[str(square)] == "df":
                start_point = (
                    left_x + (square[1] - 1) * square_length,
                    top_y + square[0] * square_length,
                )
                end_point = (
                    left_x + square[1] * square_length,
                    top_y + (square[0] - 1) * square_length,
                )
            else:
                start_point = (
                    left_x + (square[1] - 1) * square_length,
                    top_y + (square[0] - 1) * square_length,
                )
                end_point = (
                    left_x + square[1] * square_length,
                    top_y + square[0] * square_length,
                )

            pygame.draw.line(win, "red", start_point, end_point)

    def render(self, win):
        win_width, win_height = win.get_size()
        square_length = self.grid_length / self.grid_size
        left_x = win_width / 2 - self.grid_length / 2
        right_x = win_width / 2 + self.grid_length / 2
        top_y = win_height / 2 - self.grid_length / 2
        bottom_y = win_height / 2 + self.grid_length / 2
        topology_line_dim = 20
        piece_size = square_length * 0.3

        # Vertical Grid Lines
        for line_num in range(self.grid_size + 1):
            line_x = left_x + line_num * square_length

            if self.is_adjacency_map:
                pygame.draw.line(
                    win,
                    "blue",
                    (line_x, top_y - square_length),
                    (line_x, bottom_y + square_length),
                )

            pygame.draw.line(win, "black", (line_x, top_y), (line_x, bottom_y))

        # Horizontal Grid Lines
        for line_num in range(self.grid_size + 1):
            line_y = top_y + line_num * square_length

            if self.is_adjacency_map:
                pygame.draw.line(
                    win,
                    "blue",
                    (left_x - square_length, line_y),
                    (right_x + square_length, line_y),
                )

            pygame.draw.line(win, "black", (left_x, line_y), (right_x, line_y))

        # Top & Bottom Topology Arrows
        if self.topology[0] != 0:
            end_pos = (win_width / 2 + topology_line_dim / 2, top_y)
            pygame.draw.line(
                win,
                "red",
                (win_width / 2 - topology_line_dim / 2, top_y - topology_line_dim),
                end_pos,
            )
            pygame.draw.line(
                win,
                "red",
                (win_width / 2 - topology_line_dim / 2, top_y + topology_line_dim),
                end_pos,
            )

            if self.topology[0] == 1:
                end_pos = (win_width / 2 + topology_line_dim / 2, bottom_y)
                pygame.draw.line(
                    win,
                    "red",
                    (
                        win_width / 2 - topology_line_dim / 2,
                        bottom_y - topology_line_dim,
                    ),
                    end_pos,
                )
                pygame.draw.line(
                    win,
                    "red",
                    (
                        win_width / 2 - topology_line_dim / 2,
                        bottom_y + topology_line_dim,
                    ),
                    end_pos,
                )
            else:
                end_pos = (win_width / 2 - topology_line_dim / 2, bottom_y)
                pygame.draw.line(
                    win,
                    "red",
                    (
                        win_width / 2 + topology_line_dim / 2,
                        bottom_y - topology_line_dim,
                    ),
                    end_pos,
                )
                pygame.draw.line(
                    win,
                    "red",
                    (
                        win_width / 2 + topology_line_dim / 2,
                        bottom_y + topology_line_dim,
                    ),
                    end_pos,
                )

        # Left & Right Topology Arrows
        if self.topology[1] != 0:
            end_pos = (left_x, win_height / 2 - topology_line_dim / 2)
            pygame.draw.line(
                win,
                "red",
                (left_x - topology_line_dim, win_height / 2 + topology_line_dim / 2),
                end_pos,
            )
            pygame.draw.line(
                win,
                "red",
                (left_x + topology_line_dim, win_height / 2 + topology_line_dim / 2),
                end_pos,
            )

            if self.topology[1] == 1:
                end_pos = (right_x, win_height / 2 - topology_line_dim / 2)
                pygame.draw.line(
                    win,
                    "red",
                    (
                        right_x - topology_line_dim,
                        win_height / 2 + topology_line_dim / 2,
                    ),
                    end_pos,
                )
                pygame.draw.line(
                    win,
                    "red",
                    (
                        right_x + topology_line_dim,
                        win_height / 2 + topology_line_dim / 2,
                    ),
                    end_pos,
                )
            else:
                end_pos = (right_x, win_height / 2 + topology_line_dim / 2)
                pygame.draw.line(
                    win,
                    "red",
                    (
                        right_x - topology_line_dim,
                        win_height / 2 - topology_line_dim / 2,
                    ),
                    end_pos,
                )
                pygame.draw.line(
                    win,
                    "red",
                    (
                        right_x + topology_line_dim,
                        win_height / 2 - topology_line_dim / 2,
                    ),
                    end_pos,
                )

        # Noughts & Crosses
        for r, row in enumerate(self.grid):
            for c, square in enumerate(row):
                if self.grid[r][c] == 0:
                    continue

                centre = (
                    left_x + (c - 0.5) * square_length,
                    top_y + (r - 0.5) * square_length,
                )
                if 1 <= r <= self.grid_size and 1 <= c <= self.grid_size:
                    colour = "black"
                else:
                    colour = "blue"

                if self.grid[r][c] == 2:
                    pygame.draw.circle(win, colour, centre, piece_size, 1)
                else:
                    pygame.draw.line(
                        win,
                        colour,
                        (centre[0] - piece_size, centre[1] - piece_size),
                        (centre[0] + piece_size, centre[1] + piece_size),
                    )
                    pygame.draw.line(
                        win,
                        colour,
                        (centre[0] - piece_size, centre[1] + piece_size),
                        (centre[0] + piece_size, centre[1] - piece_size),
                    )
