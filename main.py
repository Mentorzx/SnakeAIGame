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


def gameOver(snake: tuple[list[int]], border: tuple[list[int]], display_range: int, time_game_fps: int, score: int) -> None:
    """ Return the game over screen an quit game if some rule of lose is cacthed """
    if game.win(snake, display_range):
        MessageBox = windll.user32.MessageBoxW
        if MessageBox(None, f'You Win!!! Score: {score}.', 'Game Over', 5) == 2:
            quit()
            exit()
        else:
            program(name, display_range, time_game_fps)
    elif game.lose(list(snake)[0], tuple(snake), border):
        # game.record_move_file(record)
        MessageBox = windll.user32.MessageBoxW
        if MessageBox(None, 'You lose', 'Game Over', 5) == 2:
            quit()
            exit()
        else:
            program(name, display_range, time_game_fps)


def program(name: str, display_range: int, time_game_fps: int):
    """ Main function of the game that execute and display the hole game """
    init()
    screen = display.set_mode((display_range, display_range))
    display.set_caption(name)
    snake, snake_skin, apple, apple_pos, border = game.constructs(
        display_range)
    clock = time.Clock()
    snake_direction = LEFT
    score = 0
    astar = players.a_star.AStar()
    monteCarlo = players.monte_carlo.MonteCarlo()
    record = []
    while True:
        game.display_score(screen, score)
        clock.tick(time_game_fps)  # refresh rate

        eventAI = astar.getKey(apple_pos, tuple(snake),
                               snake_direction, border)
        snake_direction = game.control(eventAI, snake_direction)
        # snake_direction = monteCarlo.control(display_range, snake, apple_pos, border, snake_direction)
        game.inputKey(snake_direction)

        snake, apple_pos, snake, score = game.snakeMoviment(
            tuple(snake), snake_direction, apple_pos, display_range, score)

        record.append((snake_direction, apple_pos))

        gameOver(snake, border, display_range, time_game_fps, score)

        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)

        for pos in snake:
            screen.blit(snake_skin, pos)
        display.update()


if __name__ == '__main__':
    name = 'Snake AI'
    time_game = 200
    display_range = 200

    program(name, display_range, time_game)
