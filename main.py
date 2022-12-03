import sys
import random
import ctypes
import pygame
import monte_carlo as monte_carlo
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
import time


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
    if event.type == KEYDOWN:
        if (event.key == K_UP) and (direction != DOWN):
            direction = UP
        if (event.key == K_DOWN) and (direction != UP):
            direction = DOWN
        if (event.key == K_LEFT) and (direction != RIGHT):
            direction = LEFT
        if (event.key == K_RIGHT) and (direction != LEFT):
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


def program(name: str, display_range: int, time_game_fps: int, player_control):
    pygame.init()
    screen = pygame.display.set_mode((display_range, display_range))
    pygame.display.set_caption(name)
    snake, snake_skin, apple, apple_pos, border = constructs(
        display_range)
    clock = pygame.time.Clock()
    snake_direction = LEFT
    score = 0

    while True:
        # --- mostra a pontuação na tela ---
        display_score(screen, score)

        # --- refresh rate ---
        clock.tick(time_game_fps)
        # time.sleep(1)

        # --- inputs do teclado ---
        for event in pygame.event.get():
            # procura por comandos de saida do jogo
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # --- controle manual ---
            # snake_direction = control(event, snake_direction)

        # --- controle AI ---
        snake_direction = player_control(display_range, snake, apple_pos, border, snake_direction)

        # coloquei o movimento antes da colisão para que a cobra não entre na parede,
        # pra que ela cresça no frame que come a maçâ
        # é importante que ela coma a maça imediatamente pra que a próxima maça sejá criada e sirva de guia para a cobra
        # --- movimento da cobra ---
        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i-1][0], snake[i-1][1])
        snake = motor_snake(snake_direction, snake)  # type: ignore

        # --- colisões ---
        if collision(snake[0], tuple(snake[1:])) or collision(snake[0], border):
            MessageBox = ctypes.windll.user32.MessageBoxW
            if MessageBox(None, 'You lose', 'Game Over', 5) == 2:
                pygame.quit()
                sys.exit()
            else:
                program(name, display_range, time_game, player_control)  # Manipulate to AI

        # --- maçã ---
        if collision(snake[0], tuple([apple_pos])):
            apple_pos = on_grid_random(display_range)
            score += 1  # Manipulate to AI
            snake.append((0, 0))

        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)

        for pos in snake:
            screen.blit(snake_skin, pos)

        pygame.display.update()


if __name__ == '__main__':
    name = 'Snake AI'
    time_game = 10
    display_range = 200

    program(name, display_range, time_game, monte_carlo.control)
