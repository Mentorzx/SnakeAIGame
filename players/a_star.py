from random import randrange
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from game import lose, getPossibleMoves


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Agent:
    DIRECTIONS = [[10, 0], [-10, 0], [0, 10], [0, -10]]
    current_path = []

    @staticmethod
    def manhattenDistance(snake_position: tuple[int, int], apple_position: tuple[int, int]) -> int:
        return abs(snake_position[0] - apple_position[0]) + abs(
            snake_position[1] - apple_position[1]
        )

    @staticmethod
    def reconstructPath(came_from: dict, current: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Will return an array containing the optimal path
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        print(f"path: {path}")
        return path

    @staticmethod
    def getNeighbors(snake: tuple[list[int]], current: tuple[int, int], border: tuple[list[int]], display_range: int) -> list[tuple[int, int]]:
        directions = getPossibleMoves(current)
        neighbors = [
            (
                current[0] + directions[i][0],
                current[1] + directions[i][1],
            )
            for i in range(4)
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
                distances.append((fn, path))
        return distances

    def getKey(self, apple: tuple[int, int], snake: tuple[list[int]], snake_direction: int, objects: tuple) -> int:
        """ Returns the next step """
        distances = self.getDistances(apple, snake[0], snake, objects)
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
