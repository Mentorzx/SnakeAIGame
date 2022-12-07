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
    # monteCarlo = players.monte_carlo.MonteCarlo()
    # save_number = None
    while True:
        game.display_score(screen, score)
        clock.tick(time_game_fps)  # refresh rate
        score, apple_pos, snake = game.takeApple(
            snake, apple_pos, display_range, score)
        eventAI = astar.getKey(apple_pos, snake, snake_direction, border)
        snake_direction = game.control(eventAI, snake_direction)
        #snake_direction = monteCarlo.control(display_range, snake, apple_pos, border, snake_direction)
        #save_number = game.save_move_file(save_number, snake_direction, apple_pos)
        game.inputTeclado(snake_direction)
        snake = game.snakeMoviment(snake, snake_direction)
        if game.lose(list(snake)[0], snake, border):
            game.save_death()
            MessageBox = windll.user32.MessageBoxW
            if MessageBox(None, 'You lose', 'Game Over', 5) == 2:
                quit()
                exit()
            else:
                program(name, display_range, time_game_fps)  # Manipulate to AI
        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)
        for pos in snake:
            screen.blit(snake_skin, pos)
        display.update()


if __name__ == '__main__':
    name = 'Snake AI'
    time_game = 100
    display_range = 200

    program(name, display_range, time_game)
