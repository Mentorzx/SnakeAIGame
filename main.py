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
    save_number = None
    while True:
        # --- mostra a pontuação na tela ---
        game.display_score(screen, score)

        # --- refresh rate ---
        clock.tick(time_game_fps)

        # --- maçã ---
        apple_pos, score = game.takeApple(snake, apple_pos, display_range, score)
            
        # --- controle AI ---
        eventAI = astar.getKey(apple_pos, snake, snake_direction, border)
        snake_direction = game.control(eventAI, snake_direction)
        #snake_direction = monteCarlo.control(display_range, snake, apple_pos, border, snake_direction)
        #save_number = game.save_move_file(save_number, snake_direction, apple_pos)

        # --- inputs do teclado ---
        game.inputTeclado(snake_direction)

        # --- movimento da cobra ---
        game.snakeMoviment(snake, snake_direction)

        # --- colisões ---
        if game.lose(snake[0], snake, border):
            game.save_death(save_number)
            MessageBox = ctypes.windll.user32.MessageBoxW
            if MessageBox(None, 'You lose', 'Game Over', 5) == 2:
                pygame.quit()
                sys.exit()
            else:
                program(name, display_range, time_game_fps)  # Manipulate to AI
            
        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)
        for pos in snake:
            screen.blit(snake_skin, pos)

        pygame.display.update()

if __name__ == '__main__':
    name = 'Snake AI'
    time_game = 100
    display_range = 200

    program(name, display_range, time_game)
