import game
import players.a_star
from sys import exit
from ctypes import windll
from pygame import init, quit, display, time

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
BLACK, WHITE, RED, GREEN, BLUE, ORANGE, YELLOW, INDIGO, PURPLE, TURQUOISE = (0, 0, 0), (255, 255, 255), (
    255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 127, 0), (255, 255, 0), (75, 0, 130), (160, 32, 240), (64, 224, 208)


def gameOver(snake: tuple[list[int]], border: tuple[list[int]], display_range: int, time_game_fps: int, score: int, start_time: int, color_background: tuple[int, int, int] = BLACK, color_infos: tuple[int, int, int] = BLUE, color_apple: tuple[int, int, int] = RED, color_snake: tuple[int, int, int] = WHITE, color_snake_border: tuple[int, int, int] = BLACK) -> None:
    """ Return the game over screen an quit game if some rule of lose is cacthed """
    decision = 0
    MessageBox = windll.user32.MessageBoxW
    if game.win(snake, display_range):
        decision = MessageBox(
            None, f'You Win!!! Score: {score}.', f'Game Over in {game.timeinGame(start_time)} minutes.', 5)
    elif game.lose(list(snake)[0], tuple(snake), border):
        decision = MessageBox(
            None, f'You lose. Score: {score}', f'Game Over at {game.timeinGame(start_time)} minutes.', 5)
    if decision == 2:
        quit()
        exit()
    elif decision == 4:
        program(name, display_range, time_game_fps, color_background,
                color_infos, color_apple, color_snake, color_snake_border)


def program(name: str, display_range: int, time_game_fps: int, color_background: tuple[int, int, int] = BLACK, color_infos: tuple[int, int, int] = BLUE, color_apple: tuple[int, int, int] = RED, color_snake: tuple[int, int, int] = WHITE, color_snake_border: tuple[int, int, int] = BLACK):
    """ Main function of the game that execute and display the hole game """
    init()
    screen = display.set_mode((display_range, display_range))
    display.set_caption(name)
    snake, snake_skin, apple, apple_pos, border = game.constructs(
        display_range, color_snake, color_apple)
    clock = time.Clock()
    start_time = time.get_ticks()
    snake_direction = LEFT
    score = 0
    astar = players.a_star.AStar()
    while True:
        # region Input
        eventAI = astar.getKey(apple_pos, tuple(snake),
                               snake_direction, border)
        snake_direction = game.control(eventAI, snake_direction)
        game.inputKey(snake_direction)
        # endregion
        snake, apple_pos, score = game.snakeMoviment(
            tuple(snake), snake_direction, apple_pos, display_range, score)
        # region Screen/Display
        game.display_screen(screen, score, clock, time_game_fps, snake, snake_skin, apple,
                            apple_pos, start_time, color_background, color_snake_border, color_infos)
        display.update()
        # endregion
        gameOver(snake, border, display_range,
                 time_game_fps, score, start_time, color_background, color_infos, color_apple, color_snake, color_snake_border)


if __name__ == '__main__':
    name = 'Snake AI'
    display_range = 300
    time_game = 30
    color_background = BLACK
    color_infos = TURQUOISE
    color_apple = RED
    color_snake = WHITE
    color_snake_border = BLACK

    program(name, display_range, time_game, color_background,
            color_infos, color_apple, color_snake, color_snake_border)
