import sys
import ctypes
import pygame
from pygame.locals import KEYDOWN, QUIT
import players.monte_carlo
import players.a_star
import game
import time

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def display_score(screen, score):
    pygame.font.init()
    font = pygame.font.SysFont('arial', 30)
    text = font.render(str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()


def program(name: str, display_range: int, time_game_fps: int):
    pygame.init()
    screen = pygame.display.set_mode((display_range, display_range))
    pygame.display.set_caption(name)
    snake, snake_skin, apple, apple_pos, border = game.constructs(
        display_range)
    clock = pygame.time.Clock()
    snake_direction = LEFT
    score = 0

    astar = players.a_star.AStar()
    monteCarlo = players.monte_carlo.MonteCarlo()

    while True:
        # --- mostra a pontuação na tela ---
        display_score(screen, score)

        # --- refresh rate ---
        clock.tick(time_game_fps)

        # coloquei o movimento antes da colisão para que a cobra não entre na parede,
        # pra que ela cresça no frame que come a maçâ
        # é importante que ela coma a maça imediatamente pra que a próxima maça sejá criada e sirva de guia para a cobra
        # --- movimento da cobra ---
        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i-1][0], snake[i-1][1])
        snake = game.motor_snake(snake_direction, snake)  # type: ignore
        # --- colisões ---
        if game.collision(snake[0], tuple(snake[1:])) or game.collision(snake[0], border):
            MessageBox = ctypes.windll.user32.MessageBoxW
            if MessageBox(None, 'You lose', 'Game Over', 5) == 2:
                pygame.quit()
                sys.exit()
            else:
                program(name, display_range, time_game_fps)  # Manipulate to AI

        # --- maçã ---
        if game.collision(snake[0], tuple([apple_pos])):
            apple_pos = game.on_grid_random(display_range)
            score += 1  # Manipulate to AI
            snake.append((0, 0))
            
        # --- controle AI ---
        #eventAI = astar.getKey(apple_pos, snake, snake_direction, border)
        #snake_direction = game.control(eventAI, snake_direction)

        start = time.perf_counter()
        snake_direction = monteCarlo.control(display_range, snake, apple_pos, border, snake_direction)
        end = time.perf_counter()

        print(round(end - start, 2))

        # --- inputs do teclado ---
        for event in pygame.event.get():
            # procura por comandos de saida do jogo
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # --- controle manual ---
            if event.type == KEYDOWN:
                snake_direction = game.control(event.key, snake_direction)
            
        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)
        for pos in snake:
            screen.blit(snake_skin, pos)

        pygame.display.update()

if __name__ == '__main__':
    name = 'Snake AI'
    time_game = 100
    display_range = 300

    program(name, display_range, time_game)
