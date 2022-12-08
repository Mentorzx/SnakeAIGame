from random import randrange
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from game import lose, getPossibleMoves
#from queue import PriorityQueue


class AStar:
    """
     A star algorithm implementation
     f(n) = g(n) + h(n)
     """

    def __init__(self):
        self.paths = [
            K_RIGHT,
            K_LEFT,
            K_UP,
            K_DOWN
        ]
        self.invalid = {
            K_UP: K_DOWN,
            K_DOWN: K_UP,
            K_LEFT: K_RIGHT,
            K_RIGHT: K_LEFT
        }

        self.moves = 0

    def getDistances(self, goal: tuple[int, int], current: list, snake: tuple[list[int]], objects: tuple[list[int]]) -> list:
        """ Finding distance for each path """
        # distances = PriorityQueue()
        distances = []
        self.moves += 1
        possible_moves = getPossibleMoves(snake[0])
        for path in possible_moves:
            x = None
            y = None
            goal_x = goal[0]
            goal_y = goal[1]
            if path is K_UP:
                x = current[0]
                y = current[1] - 10
            elif path is K_DOWN:
                x = current[0]
                y = current[1] + 10
            elif path is K_RIGHT:
                x = current[0] + 10
                y = current[1]
            elif path is K_LEFT:
                x = current[0] - 10
                y = current[1]
            if (x is not None) and (y is not None):
                if lose([x, y], snake, objects):
                    continue
                gn = self.moves
                hn = abs(x - goal_x) + abs(y - goal_y)
                fn = gn + hn
                # add to queue
                # distances.put((fn, path))
                distances.append((fn, path))
        return distances

    def getKey(self, apple: tuple[int, int], snake: tuple[list[int]], snake_direction: int, objects: tuple) -> int:
        """ Returns the next step """
        distances = self.getDistances(apple, snake[0], snake, objects)
        # if distances.qsize() == 0:
        if len(distances) == 0:
            return snake_direction
        index = 0
        if len(distances) == 2:
            if distances[0][0] == distances[1][0]:
                index = randrange(len(distances))
            elif distances[0][0] < distances[1][0]:
                index = 0
            else:
                index = 1
        return distances[index][1]
       # return distances.get()[1]
