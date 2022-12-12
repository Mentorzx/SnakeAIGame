from random import randrange
from threading import Lock
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from pygame import surface
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from game import collision, motor_snake, on_grid_random, lose

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
INVALIDE_DIRECTION = 5


class MonteCarlo ():
    def __init__(self):
        self.lock = Lock()
        self.paths = [
            RIGHT,
            LEFT,
            UP,
            DOWN
        ]

    # Manipulate to AI
    def control(self, display_range: int, snake: tuple[list[int]], apple_pos: tuple[int, int], border, snake_direction: int) -> int:
        score_map = [(0, 0), (0, 0), (0, 0), (0, 0)]
        parans = [display_range, snake, apple_pos,
                  border, snake_direction, score_map]

        # --- chamados dos bots ---
        with ThreadPoolExecutor(max_workers=15) as executor:
            for index in range(15000):
                executor.submit(self.thread_program, display_range, snake,
                                apple_pos, border, snake_direction, score_map, index)

        # --- decisão de direção ---
        highest_score = -99999999
        score_average = []
        for i in range(4):
            if score_map[i][0] != 0:
                # average = round(score_map[i][1]/score_map[i][0], 1)
                average = score_map[i][1]
                score_average.append((i, round(average, 1)))
                if highest_score < average:
                    highest_score = average

        # direção aleatoria dentre as com maior pontuação
        pool = []
        for i in score_average:
            if i[1] == highest_score:
                pool.append(i[0])

        rand_idx = randrange(len(pool))
        return pool[rand_idx]

    def thread_program(self, display_range: int, snake, apple_pos, border, snake_direction, score_map, index):
        first, score = self.program(
            display_range, snake, apple_pos, border, snake_direction)
        with self.lock:
            score_map[first] = score_map[first][0] + 1, score_map[first][1] + score

    def control_AI(self, direction: int, snake: tuple[list[int]], object: tuple[list[int]]):
        # pega a posição da cabeça
        current = snake[0]

        # lista de movimentos possiveis
        move_list = self.getPossibleMoves(current)

        # confere se esse movimento vai bater
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
            if (x is not None) and (y is not None) and lose([x, y], snake, object):
                move_list.remove(move)
                continue

        # se nao tiver movimentos so continua em frente
        if not move_list:
            return direction

        # direção aleatoria dentre as diponiveis
        rand_idx = randrange(len(move_list))
        return move_list[rand_idx]

    def program(self, display_range: int, snake: tuple[list[int]], apple_pos: tuple[int, int], border: tuple[list[int]], snake_direction: int) -> tuple:
        snake_bot = list(deepcopy(snake))
        snake_bot_direction = deepcopy(snake_direction)
        apple_bot_pos = deepcopy(apple_pos)
        energy = ((display_range/10) ** 2)
        apple_count = 0
        first_move = None
        while True:
            # --- controle AI ---
            snake_bot_direction = self.control_AI(
                snake_bot_direction, snake, border)

            # guarda o primeiro movimento para a decisão final
            if first_move is None:
                first_move = snake_bot_direction

            # --- movimento da cobra ---
            for i in range(len(snake_bot) - 1, 0, -1):
                list(snake_bot)[i] = [snake_bot[i-1][0], snake_bot[i-1][1]]
            snake_bot = motor_snake(
                snake_bot_direction, tuple(snake_bot))

            # --- maçã ---
            if collision(tuple(snake_bot[0]), apple_bot_pos):
                apple_count += 10  # Manipulate to AI

                return first_move, apple_count
            else:
                energy -= 1

            # --- colisões ---
            if lose(snake[0], snake, border):
                return first_move, apple_count

            if energy < 0:
                return first_move, apple_count


    def getPossibleMoves(self, current: list[int]) -> list[int]:
        """ Return a possible moviment of the object based in the position """
        possible_moves = []
        if (current[0]/10) % 2 == 0:
            possible_moves.append(DOWN)
        if (current[0]/10) % 2 == 1:
            possible_moves.append(UP)
        if (current[1]/10) % 2 == 0:
            possible_moves.append(LEFT)
        if (current[1]/10) % 2 == 1:
            possible_moves.append(RIGHT)
        return possible_moves
