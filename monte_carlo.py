import players.Player as player
import main as m
import copy
import random

import concurrent.futures
import threading

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

lock = threading.Lock()

def control(display_range, snake, apple_pos, border, snake_direction: int) -> int:  # Manipulate to AI
    
    score_map = [(0, 0), (0, 0), (0, 0)]

    parans = [display_range, snake, apple_pos, border, snake_direction, score_map]

    #print(f"start thread {score_map}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for index in range(1000):
            executor.submit(thread_program, display_range, snake, apple_pos, border, snake_direction, score_map, index)
    #print(f"end thread {score_map}")


    highest_score = -10000000000000
    move = 1
    for i in range(3):
        if score_map[i][0] != 0:
            average = score_map[i][1]/score_map[i][0]
            if highest_score < average:
                highest_score = average
                move = i
        
    return player.redirect(move, snake_direction)  # type: ignore
    
def control_AI(move, direction, snake):
    while True:
        direction = player.redirect(move, direction)
        if (snake[0]/10)%2 == 0:
            direction == DOWN
            break
        if (snake[0]/10)%2 == 1:
            direction == UP
            break
        if (snake[1]/10)%2 == 0:
            direction == RIGHT
            break
        if (snake[1]/10)%2 == 1:
            direction == LEFT
            break
        
    # colli = player.find_possible_collision(snake[0])   # type: ignore

    # if colli != False and colli == direction:
    #     return super().redirect(2, direction) 

    # if snake[0][0] != apple_pos[0]:
    #     if snake[0][0] > apple_pos[0]:
    #         return LEFT  
    #     if snake[0][0] < apple_pos[0]:
    #         return RIGHT 
    # if snake[0][1] != apple_pos[1]:
    #     if snake[0][1] > apple_pos[1]:
    #         return UP   
    #     if snake[0][1] < apple_pos[1]:
    #         return DOWN 
    
    # return direction
    # return redirect(input, direction)
    

def program(display_range: int, snake, apple_pos, border, snake_direction) -> tuple:

    snake_bot = copy.deepcopy(snake)
    snake_bot_direction = copy.deepcopy(snake_direction)
    apple_bot_pos = apple_pos
    
    valor_apple = 20
    valor_step = 0
    valor_death = -100
    score_bot = 200
    first_move = None

    while True:

        # --- controle AI ---
        while True:
            snake_change = random.randint(0, 2)
            if first_move is None:
                first_move = snake_change
            snake_bot_direction = player.redirect(snake_change, snake_bot_direction)
            if (snake[0][0]/10)%2 == 0:
                snake_bot_direction == DOWN
                break
            if (snake[0][0]/10)%2 == 1:
                snake_bot_direction == DOWN
                break

        # --- movimento da cobra ---
        for i in range(len(snake_bot) - 1, 0, -1):
            snake_bot[i] = (snake_bot[i-1][0], snake_bot[i-1][1])
        snake_bot = m.motor_snake(snake_bot_direction, snake_bot)  # type: ignore

        # --- maçã ---
        if m.collision(snake_bot[0], tuple([apple_bot_pos])):
            apple_bot_pos = m.on_grid_random(display_range)
            score_bot += valor_apple  # Manipulate to AI
            snake_bot.append((0, 0))
        else:
            score_bot += valor_step

        # --- colisões ---
        if m.collision(snake_bot[0], tuple(snake_bot[1:])) or m.collision(snake_bot[0], border):
            score_bot += valor_death
            return first_move, score_bot
        
        if score_bot < 0:
            return first_move, score_bot
        
def thread_program ( display_range: int, snake, apple_pos, border, snake_direction, score_map, index):
    first, score = program(display_range, snake, apple_pos, border, snake_direction)
    with lock:
        score_map[first] = score_map[first][0] + 1, score_map[first][1] + score