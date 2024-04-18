class Computer:  # Class
    def __init__(self, grid, moves):
        self.grid = grid
        self.moves = moves

    def count_outcomes(
        self, n, outcomes, player=1
    ):  # Recursive & complex user-defined algorithm
        size = self.grid.grid_size
        for row in range(1, size + 1):
            for col in range(1, size + 1):
                if self.grid.grid[row][col] == 0:
                    self.grid.move([row, col], player)
                    outcome = self.grid.check_end([row, col], player)
                    if type(outcome) == list:
                        outcomes.append(player)  # List Operations

                    if outcome is not False or n <= 1:
                        self.grid.previous_move(True)
                    else:
                        outcomes = self.count_outcomes(
                            n - 1, outcomes, 0 ** (player - 1) + 1
                        )
                        self.grid.previous_move(True)

        return outcomes

    def get_best_move(self):
        high_score = float("-inf")
        for row in range(1, self.grid.grid_size + 1):
            for col in range(1, self.grid.grid_size + 1):
                if self.grid.grid[row][col] == 0:
                    self.grid.move([row, col], 2)
                    outcomes = self.count_outcomes(self.moves - 1, [])
                    if len(outcomes) == 0:
                        score = 0
                    else:
                        score = (outcomes.count(2) - outcomes.count(1)) / len(outcomes)

                    if score > high_score:
                        high_score = score
                        best_move = (row, col)
                    self.grid.previous_move(True)

        return best_move
