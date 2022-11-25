import pygame
import random
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT


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


def control(event, direction: int) -> int:
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


def redirect(input: int, direction: int) -> int:
    if direction == UP:
        if input == 0:
            return LEFT 
        if input == 1:
            return direction
        if input == 2:
            return RIGHT 
    if direction == DOWN:
        if input == 0:
            return RIGHT 
        if input == 1:
            return direction
        if input == 2:
            return LEFT 
    if direction == LEFT:
        if input == 0:
            return DOWN 
        if input == 1:
            return direction
        if input == 2:
            return UP 
    if direction == RIGHT:
        if input == 0:
            return UP 
        if input == 1:
            return direction
        if input == 2:
            return DOWN 

def find_possible_collision(object1):
    
    if object1[0]-10 < 0:
        return LEFT
    if object1[0]+10 > 590:
        return RIGHT   
    if object1[1]-10 < 0: 
        return UP
    if object1[1]+10 > 590:
        return DOWN
    
    return False



def control_AI(direction: int, snake, apple_pos) -> int:
    colli = find_possible_collision(snake[0])

    if colli != False and colli == direction:
        return redirect(2, direction)

    if snake[0][0] != apple_pos[0]:
        if snake[0][0] > apple_pos[0]:
            return LEFT
        if snake[0][0] < apple_pos[0]:
            return RIGHT
    if snake[0][1] != apple_pos[1]:
        if snake[0][1] > apple_pos[1]:
            return UP
        if snake[0][1] < apple_pos[1]:
            return DOWN
    
    return direction


    return redirect(input, direction)


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
        
        snake_direction = control_AI(snake_direction, snake, apple_pos)
        
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
