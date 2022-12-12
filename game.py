import sys
import pygame
from random import randint
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
from pygame import draw, Rect


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
BLACK, WHITE, RED, GREEN, BLUE, ORANGE, YELLOW, INDIGO, PURPLE, TURQUOISE = (0, 0, 0), (255, 255, 255), (
    255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 127, 0), (255, 255, 0), (75, 0, 130), (160, 32, 240), (64, 224, 208)


def on_grid_random(display_range: int) -> tuple[int, int]:
    """ Return a randomly position (int, int) to the apple """
    x = randint(0, display_range - 10)
    y = randint(0, display_range - 10)
    return (x//10 * 10, y//10 * 10)


def getNewApple(snake: tuple[list[int]], apple_pos: tuple[int, int], display_range: int) -> tuple[int, int]:
    """ Return a new position for an apple """
    while collision(apple_pos, snake):
        apple_pos = on_grid_random(display_range)
    return apple_pos


def collision(object1: tuple, object2: tuple) -> bool:
    """ Return True if have collision with 2 objects in somewhere
    Return False if don't have any collision of 2 objects """
    return (list(object1) in list(object2)) or (list(object1) == list(object2))


def lose(pos: list[int], snake: tuple[list[int]], border: tuple[list[int]]) -> bool:
    """ Return True if the snake has passed in one or more conditionals of lose
    Return False if the snake don't passed in any conditionals of lose """
    return collision(tuple(pos), snake[1:]) or collision(tuple(pos), border)


def win(snake: tuple[list[int]], display_range: int) -> bool:
    len_display = (display_range//10)**2
    return len(snake) >= len_display


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
    """ Return a new position for the snake head based in your direction and actual position """
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


def snakeMoviment(snake: tuple[list[int]], snake_direction: int, apple_pos: tuple[int, int], display_range: int, score: int) -> tuple[tuple[list[int]], tuple[int, int], int]:
    """ Realize the moviment of the snake and Return new random position for the apple and sum the score """
    snake_list = list(snake)
    snake = motor_snake(snake_direction, tuple(snake))

    # region Eat apple
    gotApple = collision(tuple(snake[0]), apple_pos)
    if gotApple:
        snake_list.append([0, 0])
    # endregion

    # region Move body
    for i in range(len(snake_list) - 1, 0, -1):
        snake_list[i] = snake_list[i-1]
    snake_list[0] = [snake[0][0], snake[0][1]]
    snake = tuple(snake_list)
    # endregion

    # region New apple
    if gotApple:
        apple_pos = apple_pos if win(snake, display_range) else getNewApple(
            snake, apple_pos, display_range)
        score += 1
    # endregion

    return snake, apple_pos, score


def timeinGame(start_time: int) -> str:
    counting_time = pygame.time.get_ticks() - start_time
    counting_minutes = str(counting_time//60000).zfill(2)
    counting_seconds = str((counting_time % 60000)//1000).zfill(2)
    counting_millisecond = str(counting_time % 1000).zfill(3)
    counting_string = "%s:%s:%s" % (
        counting_minutes, counting_seconds, counting_millisecond)
    return counting_string


def display_info(screen: pygame.surface.Surface, score: int, start_time: int, color_infos: tuple[int, int, int] = BLUE) -> None:
    """ Displays time on the screen """
    pygame.font.init()
    font = pygame.font.SysFont('arial', 30)
    text = font.render(str(timeinGame(start_time)),
                       True, color_infos)
    screen.blit(text, (10, 10))
    text = font.render(str(score), True, color_infos)
    screen.blit(text, (10, 50))
    pygame.display.flip()


def display_screen(screen, score, clock, time_game_fps, snake, snake_skin, apple, apple_pos, start_time, color_background, color_snake_border, color_infos):
    clock.tick(time_game_fps)  # refresh rate

    screen.fill(color_background)
    screen.blit(apple, apple_pos)

    for pos in snake:
        snake_border = Rect(pos[0], pos[1], 10, 10)
        draw.rect(snake_skin, color_snake_border, snake_border, 1)
        screen.blit(snake_skin, pos)

    display_info(screen, score, start_time, color_infos)


def constructs(display_range: int, color_snake: tuple[int, int, int] = WHITE, color_apple: tuple[int, int, int] = RED) -> tuple[tuple[list[int]], pygame.surface.Surface, pygame.surface.Surface, tuple[int, int], tuple[list[int]]]:
    """ Return tuples properties of the objects in the game """
    snake = [[50, 50], [60, 50], [70, 50]]
    apple_pos = on_grid_random(display_range)
    snake_skin, apple, border = subConstructs(display_range, color_snake, color_apple)
    return tuple(snake), snake_skin, apple, apple_pos, tuple(border)


def subConstructs(display_range: int, color_snake: tuple[int, int, int] = WHITE, color_apple: tuple[int, int, int] = RED) -> tuple[pygame.surface.Surface, pygame.surface.Surface, tuple[list[int]]]:
    """ Return tuples properties of the objects in the game """
    snake_skin = pygame.Surface((10, 10))
    snake_skin.fill(color_snake)
    apple_pos = on_grid_random(display_range)
    apple = pygame.Surface((10, 10))
    apple.fill(color_apple)
    border = []
    for i in range(display_range-7):
        border_init = [-10, i]
        border_end = [display_range, i]
        border.extend([border_init, border_init[::-1],
                      border_end, border_end[::-1]])
    return  snake_skin, apple, tuple(border)


def inputKey(snake_direction: int) -> None:
    """ Verify if exist any input and return in game your result """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # --- controle manual ---
        if event.type == KEYDOWN:
            snake_direction = control(event.key, snake_direction)


def getPossibleMoves(current: list[int]) -> list[int]:
    """ Return a possible moviment of the object based in the position """
    possible_moves = []
    if (current[0]/10) % 2 == 0:
        possible_moves.append(K_DOWN)
    if (current[0]/10) % 2 == 1:
        possible_moves.append(K_UP)
    if (current[1]/10) % 2 == 0:
        possible_moves.append(K_LEFT)
    if (current[1]/10) % 2 == 1:
        possible_moves.append(K_RIGHT)
    return possible_moves



