import sys
import pygame
from random import randint
from collections import Counter
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def on_grid_random(display_range: int) -> tuple[int, int]:
    """ Return a randomly position int the display of something """
    x = randint(0, display_range-10)
    y = randint(0, display_range-10)
    return (x//10 * 10, y//10 * 10)


def collision(object1: tuple, object2: tuple) -> bool:
    """ Return True if have collision with 2 objects in somewhere
    Return False if don't have any collision of 2 objects """
    return (list(object1) in list(object2)) or (list(object1) == list(object2))


def takeApple(snake: tuple[list[int]], apple_pos: tuple[int, int], display_range: int, score: int) -> tuple[int, tuple[int, int], tuple[list[int]]]:
    """ Return new random position for the apple and sum the score """
    snake_list = list(snake)
    if collision(tuple(snake[0]), apple_pos):
        apple_pos = on_grid_random(display_range)
        snake_list.append([0, 0])
        score += 1  # Manipulate to AI
    return score, apple_pos, tuple(snake_list)


def lose(pos: list[int], snake: tuple[list[int]], border: tuple[list[int]]) -> bool:
    """ Return True if the snake has passed in one or more conditionals of lose
    Return False if the snake don't passed in any conditionals of lose """
    return collision(tuple(pos), snake[1:]) or collision(tuple(pos), border)


def control(event: int, direction: int) -> int:  # Manipulate to AI
    """ Return a int direction for the snake based in a number or event-number """
    if (event == K_UP) and (direction != DOWN):
        direction = UP
    if (event == K_DOWN) and (direction != UP):
        direction = DOWN
    if (event == K_LEFT) and (direction != RIGHT):
        direction = LEFT
    if (event == K_RIGHT) and (direction != LEFT):
        direction = RIGHT
    return direction


def motor_snake(direction: int, snake: tuple[list[int]]) -> tuple[list[int]]:
    """ Return a new position for the snake based in your direction and actual position """
    snake_list = list(snake)
    if direction == UP:
        snake_list[0] = [snake[0][0], snake[0][1] - 10]
    if direction == DOWN:
        snake_list[0] = [snake[0][0], snake[0][1] + 10]
    if direction == RIGHT:
        snake_list[0] = [snake[0][0] + 10, snake[0][1]]
    if direction == LEFT:
        snake_list[0] = [snake[0][0] - 10, snake[0][1]]
    return tuple(snake_list)


def snakeMoviment(snake: tuple[list[int]], snake_direction: int) -> tuple[list[int]]:
    """ Realize the moviment of the snake """
    snake_list = list(snake)
    for i in range(len(snake) - 1, 0, -1):
        snake_list[i] = [snake[i-1][0], snake[i-1][1]]
    snake_tuple = motor_snake(snake_direction, tuple(snake_list))
    return snake_tuple


def display_score(screen: pygame.surface.Surface, score: int) -> None:
    """ Displays score on the screen """
    pygame.font.init()
    font = pygame.font.SysFont('arial', 30)
    text = font.render(str(score), True, (0, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()


def constructs(display_range: int) -> tuple[tuple[list[int]], pygame.surface.Surface, pygame.surface.Surface, tuple[int, int], tuple[list[int]]]:
    """ Return tuples properties of the objects in the game """
    snake = [[50, 50], [60, 50], [70, 50]]
    snake_skin = pygame.Surface((10, 10))
    snake_skin.fill((255, 255, 255))
    apple_pos = on_grid_random(display_range)
    apple = pygame.Surface((10, 10))
    apple.fill((255, 0, 0))
    border = []
    for i in range(display_range-7):
        border_init = [-10, i]
        border_end = [display_range, i]
        border.extend([border_init, border_init[::-1],
                      border_end, border_end[::-1]])
    return tuple(snake), snake_skin, apple, apple_pos, tuple(border)


def inputTeclado(snake_direction: int) -> None:
    """ Verify if exist any input and return in game your result """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # --- controle manual ---
        if event.type == KEYDOWN:
            snake_direction = control(event.key, snake_direction)


def read_move_file(save_number: str) -> str:
    """ I don't know what this do """
    with open('save.txt', 'r') as save_file:
        lines = save_file.readlines()
    line = 0
    while lines[line] != f'save_number: {save_number}':
        line += 1
    return lines[line + 1]


def save_move_file(save_number: str, move: int, apple_pos: tuple[int, int]) -> str:
    """ I don't know what this do """
    if not save_number:
        with open('config.txt', 'r') as config_file:
            save_number = config_file.readline().strip().split(' ')[1]
        with open('config.txt', 'w') as config_file:
            config_file.write(f'save_number: {int(save_number) + 1}')
        with open('save.txt', 'a') as save_file:
            save_file.write(f'Save: {save_number} \n')
            save_file.write(f'({move}, {apple_pos}) ')
    else:
        with open('save.txt', 'a') as save_file:
            save_file.write(f'({move}, {apple_pos}) ')
    return save_number


def save_death() -> None:
    """ I don't know what this do """
    with open('save.txt', 'a') as save_file:
        save_file.write('DEATH\n\n\n')
