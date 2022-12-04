import players.Player as player
import copy
import random
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from game import collision, motor_snake, on_grid_random

import concurrent.futures
import threading

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
INVALIDE_DIRECTION = 5

class MonteCarlo ():
    def __init__(self):
        self.lock = threading.Lock()

        self.paths = [
            RIGHT,
            LEFT,
            UP,
            DOWN
        ]


    def control(self, display_range, snake, apple_pos, border, snake_direction: int) -> int:  # Manipulate to AI
        
        score_map = [(0, 0), (0, 0), (0, 0), (0, 0)]

        parans = [display_range, snake, apple_pos, border, snake_direction, score_map]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for index in range(1000):
                executor.submit(self.thread_program, display_range, snake, apple_pos, border, snake_direction, score_map, index)

        highest_score = -99999999
        move = snake_direction
        score_average = []
        for i in range(4):
            if score_map[i][0] != 0:
                average = score_map[i][1]/score_map[i][0]
                score_average.append((i, round(average, 2)))
                if highest_score < average:
                    highest_score = average
                    move = i

        print(move, score_average)
            
        return move
        #return player.redirect(move, snake_direction)  # type: ignore
        
                
    def thread_program (self, display_range: int, snake, apple_pos, border, snake_direction, score_map, index):
        first, score = self.program(display_range, snake, apple_pos, border, snake_direction)
        with self.lock:
            score_map[first] = score_map[first][0] + 1, score_map[first][1] + score

    
    def control_AI(self, direction, snake, object):
        # pega a posição da cabeça
        current = snake[0]

        #lista de movimentos possiveis
        move_list = [UP, DOWN, RIGHT, LEFT]

        # # controle direcional 
        # if ((current[0]/10)%2 == 0):
        #     move_list.append(DOWN)
        # if ((current[0]/10)%2 == 1):
        #     move_list.append(UP)
        # if ((current[1]/10)%2 == 0):
        #     move_list.append(RIGHT)
        # if ((current[1]/10)%2 == 1):
        #     move_list.append(LEFT)
        x = current[0]
        y = current[1]
        if x-10 < 0:
            move_list.remove(LEFT)
        if x+10 > object - 10:
            move_list.remove(RIGHT)   
        if y-10 < 0: 
            move_list.remove(UP)
        if y+10 > object - 10:
            move_list.remove(DOWN)
        
        #confere se esse movimento vai bater
        for move in move_list:
            x = None
            y = None
            if move is UP:
                x = current[0]
                y = current[1] - 10
            elif move is DOWN:
                x = current[0]
                y = current[1] + 10
            elif move is RIGHT:
                x = current[0] + 10
                y = current[1]
            elif move is LEFT:
                x = current[0] - 10
                y = current[1]
            if collision((x, y), tuple(snake)):
                move_list.remove(move)
                continue
                
                        
        # se nao tiver movimentos so continua em frente
        if not move_list:
            return direction
        
        # direção aleatoria dentre as diponiveis
        rand_idx = random.randrange(len(move_list))
        return move_list[rand_idx]
        

    def program(self, display_range: int, snake, apple_pos, border, snake_direction) -> tuple:

        snake_bot = copy.deepcopy(snake)
        snake_bot_direction = copy.deepcopy(snake_direction)
        apple_bot_pos = copy.deepcopy(apple_pos)

        energy = (display_range/10) * 2
        apple_count = 0
        valor_step = 0
        valor_death = 0

        first_move = None

        while True:
            # --- controle AI ---
            snake_bot_direction = self.control_AI(snake_bot_direction, snake, display_range)

            if first_move is None:
                first_move = snake_bot_direction

            # --- movimento da cobra ---
            for i in range(len(snake_bot) - 1, 0, -1):
                snake_bot[i] = (snake_bot[i-1][0], snake_bot[i-1][1])
            snake_bot = motor_snake(snake_bot_direction, snake_bot)  # type: ignore

            # --- maçã ---
            if collision(snake_bot[0], tuple([apple_bot_pos])):
                apple_bot_pos = on_grid_random(display_range)
                apple_count += 1  # Manipulate to AI
                snake_bot.append((0, 0))

                energy = (display_range/10) * 2
            else:
                energy -= 1

            # --- colisões ---
            if collision(snake_bot[0], tuple(snake_bot[1:])) or collision(snake_bot[0], border):
                return first_move, apple_count
            
            if energy < 0:
                return first_move, apple_count