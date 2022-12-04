import random
import pygame
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def on_grid_random(display_range) -> tuple[int, int]:
    x = random.randint(0, display_range-10)
    y = random.randint(0, display_range-10)
    return (x//10 * 10, y//10 * 10)


def collision(object1: tuple, object2: tuple) -> bool:
    if object1 in object2:
        return True
    return False


def constructs(display_range: int) -> tuple:
    snake = [(100, 100), (110, 100), (120, 100)]
    snake_skin = pygame.Surface((10, 10))
    snake_skin.fill((255, 255, 255))
    apple_pos = on_grid_random(display_range)
    apple = pygame.Surface((10, 10))
    apple.fill((255, 0, 0))
    border = []
    for i in range(display_range-7):
        border_init = (-10, i)
        border_end = (display_range, i)
        border.extend([border_init, border_init[::-1],
                      border_end, border_end[::-1]])
    return snake, snake_skin, apple, apple_pos, border


def control(event, direction: int) -> int:  # Manipulate to AI
    if (event == K_UP) and (direction != DOWN):
        direction = UP
    if (event == K_DOWN) and (direction != UP):
        direction = DOWN
    if (event == K_LEFT) and (direction != RIGHT):
        direction = LEFT
    if (event == K_RIGHT) and (direction != LEFT):
        direction = RIGHT
    return direction


def motor_snake(direction: int, snake: list) -> list:
    if direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])
    return snake


def display_score(screen, score):
    pygame.font.init()
    font = pygame.font.SysFont('arial', 30)
    text = font.render(str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()


def lose(pos: tuple, snake, border) -> bool:
    return collision(pos, tuple(snake[1:])) or collision(pos, border)






