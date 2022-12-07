import random
import pygame
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
import sys
import time
import ctypes


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
    snake = [(50, 50), (60, 50), (70, 50)]
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
    text = font.render(str(score), True, (0, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()


def lose(pos: tuple, snake, border) -> bool:
    return collision(pos, tuple(snake[1:])) or collision(pos, border)


def snakeMoviment(snake, snake_direction):
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])
    snake = motor_snake(snake_direction, snake) 


def inputTeclado(snake_direction):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # --- controle manual ---
        if event.type == KEYDOWN:
            snake_direction = control(event.key, snake_direction)


def takeApple(snake, apple_pos, display_range, score):
    if collision(snake[0], tuple([apple_pos])):
        apple_pos = on_grid_random(display_range)
        snake.append((0, 0))
        score += 1  # Manipulate to AI

    return apple_pos, score

def save_move_file(save_number, move, apple_pos):

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


def save_death(save_number):
    with open('save.txt', 'a') as save_file:
        save_file.write('DEATH\n\n\n')


def read_move_file(save_number):
    with open('save.txt', 'r') as save_file:
        lines = save_file.readlines()

    line = 0
    while lines[line] != f'save_number: {save_number}':
        line += 1
    
    return lines[line + 1]




