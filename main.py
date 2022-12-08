from sys import exit
from ctypes import windll
from pygame import init, quit, display, time
import game
import players.a_star
import players.monte_carlo

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def gameOver(snake: tuple[list[int]], border: tuple[list[int]], display_range: int, time_game_fps: int, score: int, start_time: int) -> None:
    """ Return the game over screen an quit game if some rule of lose is cacthed """
    decision = 0
    MessageBox = windll.user32.MessageBoxW
    if game.win(snake, display_range):
        decision = MessageBox(
            None, f'You Win!!! Score: {score}.', f'Game Over in {game.timeinGame(start_time)} minutes.', 5)
    elif game.lose(list(snake)[0], tuple(snake), border):
        # game.record_move_file(record)
        decision = MessageBox(
            None, f'You lose. Score: {score}', f'Game Over at {game.timeinGame(start_time)} minutes.', 5)
    if decision == 2:
        quit()
        exit()
    elif decision == 4:
        program(name, display_range, time_game_fps)


def program(name: str, display_range: int, time_game_fps: int):
    """ Main function of the game that execute and display the hole game """
    init()
    screen = display.set_mode((display_range, display_range))
    display.set_caption(name)
    snake, snake_skin, apple, apple_pos, border = game.constructs(
        display_range)
    clock = time.Clock()
    start_time = time.get_ticks()
    snake_direction = LEFT
    score = 0
    astar = players.a_star.AStar()
    # monteCarlo = players.monte_carlo.MonteCarlo()
    record = []
    while True:
        # region Input
        eventAI = astar.getKey(apple_pos, tuple(snake),
                               snake_direction, border)
        snake_direction = game.control(eventAI, snake_direction)
        # snake_direction = monteCarlo.control(display_range, snake, apple_pos, border, snake_direction)
        game.inputKey(snake_direction)
        # endregion

        snake, apple_pos, score = game.snakeMoviment(
            tuple(snake), snake_direction, apple_pos, display_range, score)

        record.append((snake_direction, apple_pos))

        # region Screen/Display
        clock.tick(time_game_fps)  # refresh rate

        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)
        for pos in snake:
            screen.blit(snake_skin, pos)

        game.display_info(screen, score, start_time)
        display.update()
        # endregion

        gameOver(snake, border, display_range,
                 time_game_fps, score, start_time)


if __name__ == '__main__':
    name = 'Snake AI'
    time_game = 200
    display_range = 200

    program(name, display_range, time_game)
