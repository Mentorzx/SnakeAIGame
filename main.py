import pygame
import random
from pygame.locals import *


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def on_grid_random() -> tuple[int, int]:
    x = random.randint(0, 590)
    y = random.randint(0, 590)
    return (x//10 * 10, y//10 * 10)


def collision(object1: list[int], object2: list[int]) -> bool:
    return (object1[0] == object2[0]) and (object1[1] == object2[1])


def constructs() -> tuple:
    snake = [(200, 200), (210, 200), (220, 200)]
    snake_skin = pygame.Surface((10, 10))
    snake_skin.fill((255, 255, 255))
    apple_pos = on_grid_random()
    apple = pygame.Surface((10, 10))
    apple.fill((255, 0, 0))
    return snake, snake_skin, apple, apple_pos


def control_AI(event, direction: int) -> int:
    if event.type == KEYDOWN:
        if event.key == K_UP:
            direction = UP
        if event.key == K_DOWN:
            direction = DOWN
        if event.key == K_LEFT:
            direction = LEFT
        if event.key == K_RIGHT:
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


def program(name: str, display_range: int, time_game_fps: int):
    pygame.init()
    screen = pygame.display.set_mode((display_range, display_range))
    pygame.display.set_caption(name)
    snake, snake_skin, apple, apple_pos = constructs()
    clock = pygame.time.Clock()
    snake_direction = LEFT
    while True:
        clock.tick(time_game_fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            snake_direction = control_AI(event, snake_direction)
        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0, 0))
        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i-1][0], snake[i-1][1])
        snake = motor_snake(snake_direction, snake)
        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)
        for pos in snake:
            screen.blit(snake_skin, pos)
        pygame.display.update()


if __name__ == '__main__':
    name = 'Snake AI'
    time_game_fps = 60
    display_range = 600

    program(name, display_range, time_game_fps)
