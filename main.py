from MOD import *
import pygame

pygame.init()

W, H = 800, 600
WIN = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()
FPS = 40
TOPOLOGIES = {
    "Plane": (0, 0),
    "Cylinder": (0, 1),
    "Mobius Strip": (0, -1),
    "Torus": (1, 1),
    "Klein Bottle": (1, -1),
    "Projective Plane": (-1, -1),
}


def run_menu():
    menu = Menu(W, H)  # Dynamic generation of objects
    outcome = None

    while not outcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"

        mouse_x, mouse_y = pygame.mouse.get_pos()
        outcome = menu.loop(WIN, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])

        pygame.display.update()
        CLOCK.tick(FPS)

    return outcome


def run_previous_game():
    previous_game = PreviousGame(W, H)  # Dynamic generation of objects
    outcome = None

    while not outcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"

        mouse_x, mouse_y = pygame.mouse.get_pos()
        outcome = previous_game.loop(
            WIN, mouse_x, mouse_y, pygame.mouse.get_pressed()[0]
        )

        pygame.display.update()
        CLOCK.tick(FPS)

    return outcome


def run_game(settings, moves=None):
    game = Game(W, H, settings, moves)  # Dynamic generation of objects
    outcome = None

    while not outcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if moves:
            outcome = game.loop_previous_game(
                WIN, mouse_x, mouse_y, pygame.mouse.get_pressed()[0]
            )
        else:
            outcome = game.loop_game(
                WIN, mouse_x, mouse_y, pygame.mouse.get_pressed()[0]
            )

        pygame.display.update()
        CLOCK.tick(FPS)

    return outcome


def run_settings():
    settings = Settings(W, H)
    outcome = None
    char_inp = None

    while not outcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"

            elif char_inp and event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_0]:
                    char = "0"
                elif keys[pygame.K_1]:
                    char = "1"
                elif keys[pygame.K_2]:
                    char = "2"
                elif keys[pygame.K_3]:
                    char = "3"
                elif keys[pygame.K_4]:
                    char = "4"
                elif keys[pygame.K_5]:
                    char = "5"
                elif keys[pygame.K_6]:
                    char = "6"
                elif keys[pygame.K_7]:
                    char = "7"
                elif keys[pygame.K_8]:
                    char = "8"
                elif keys[pygame.K_9]:
                    char = "9"
                else:
                    continue

                if char_inp == "Grid Size Input":
                    settings.grid_size_inp.update_input(char)
                elif char_inp == "Line Size Input":
                    settings.line_size_inp.update_input(char)
                else:
                    settings.moves_inp.update_input(char)

                char_inp = None

        mouse_x, mouse_y = pygame.mouse.get_pos()
        outcome = settings.loop(WIN, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])
        if outcome and "Input" in outcome:
            char_inp = outcome
            outcome = None

        pygame.display.update()
        CLOCK.tick(FPS)

    return outcome


def main():
    settings = [(0, 0), 3, 3, False, 3, False, "Single-Player"]

    while True:
        outcome = run_menu()

        if outcome == "Settings":
            outcome = run_settings()
            settings = outcome

        elif outcome == "Play Game":
            outcome = run_game(settings)

        elif outcome == "Previous Game":
            outcome = run_previous_game()
            if type(outcome) == int:
                topology, grid_size, line_size, is_single_player = retrieve_settings(
                    outcome
                )
                topology = TOPOLOGIES[topology]
                outcome = run_game(
                    [
                        topology,
                        grid_size,
                        line_size,
                        False,
                        settings[4],
                        settings[5],
                        "Single-Player" if is_single_player else "Multiplayer",
                    ],
                    [
                        (int(move[0][0]), int(move[0][2]))
                        for move in retrieve_moves(outcome)
                    ],
                )

        if outcome == "Quit":
            return


if __name__ == "__main__":
    main()
    pygame.quit()
