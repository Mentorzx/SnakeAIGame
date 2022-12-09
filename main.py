from sys import exit
from ctypes import windll
from pygame import init, quit, display, time, draw, Rect
import game
import record
import players.a_star
import players.monte_carlo

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
BLACK, WHITE, RED, GREEN, BLUE, ORANGE, YELLOW, INDIGO, PURPLE, TURQUOISE = (0, 0, 0), (255, 255, 255), (
    255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 127, 0), (255, 255, 0), (75, 0, 130), (160, 32, 240), (64, 224, 208)


def playback(playback_number: int, time_game_fps: int):
    init()
    display_range, snake, moves = record.recordReadStart(playback_number)
    snake_skin, apple, border = game.subConstructs(display_range)

    screen = display.set_mode((display_range, display_range))
    display.set_caption(f'Playback {playback_number}')
    
    clock = time.Clock()
    start_time = time.get_ticks()
    score = 0
    snake_direction = None
    apple_pos = None
    for m in moves:
        if m.__contains__('DEATH'):
            break

        snake_direction, apple_pos_file = record.recordReadMoveFormat(m)
        if not apple_pos:
            apple_pos = apple_pos_file
            newApple = False
        else:
            newApple = apple_pos != apple_pos_file

        snake, apple_pos, score = game.snakeMoviment(
            tuple(snake), snake_direction, apple_pos, display_range, score)

        if newApple:
            apple_pos = apple_pos_file

        # region Screen/Display
        game.display_screen(screen, score, clock, time_game_fps, snake, snake_skin, apple, apple_pos, start_time, color_background, color_snake_border, color_infos)
        display.update()
        # endregion

    record.finishPlayback(snake, display_range, border, score, start_time)


def gameOver(snake: tuple[list[int]], border: tuple[list[int]], display_range: int, time_game_fps: int, score: int, start_time: int, record_str: str, color_background: tuple[int, int, int] = BLACK, color_infos: tuple[int, int, int] = BLUE, color_apple: tuple[int, int, int] = RED, color_snake: tuple[int, int, int] = WHITE, color_snake_border: tuple[int, int, int] = BLACK) -> None:
    """ Return the game over screen an quit game if some rule of lose is cacthed """
    decision = 0
    MessageBox = windll.user32.MessageBoxW
    if game.win(snake, display_range):
        record.finishRecord(record_str, game.timeinGame(start_time))
        decision = MessageBox(
            None, f'You Win!!! Score: {score}.', f'Game Over in {game.timeinGame(start_time)} minutes.', 5)
    elif game.lose(list(snake)[0], tuple(snake), border):
        record.finishRecord(record_str, game.timeinGame(start_time))
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
    monteCarlo = players.monte_carlo.MonteCarlo()
    record_str = record.startRecord(display_range, snake)
    while True:
        # region Input
        # eventAI = astar.getKey(apple_pos, tuple(snake),
        #                        snake_direction, border)
        # snake_direction = game.control(eventAI, snake_direction)
        snake_direction = monteCarlo.control(display_range, snake, apple_pos, border, snake_direction)
        game.inputKey(snake_direction)
        # endregion

        snake, apple_pos, score = game.snakeMoviment(
            tuple(snake), snake_direction, apple_pos, display_range, score)

        # region Screen/Display
        game.display_screen(screen, score, clock, time_game_fps, snake, snake_skin, apple, apple_pos, start_time, color_background, color_snake_border, color_infos)
        display.update()
        # endregion

        record_str += record.recordMoveFormat(snake_direction, apple_pos)
        gameOver(snake, border, display_range,
                 time_game_fps, score, start_time, record_str, color_background, color_infos, color_apple, color_snake, color_snake_border)


if __name__ == '__main__':
    name = 'Snake AI'
    display_range = 60
    time_game = 10
    color_background = BLACK
    color_infos = TURQUOISE
    color_apple = RED
    color_snake = WHITE
    color_snake_border = BLACK

    program(name, display_range, time_game, color_background,
            color_infos, color_apple, color_snake, color_snake_border)

    record_number = 5
    playback(record_number, time_game)
