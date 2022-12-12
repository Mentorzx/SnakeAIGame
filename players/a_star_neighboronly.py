import math
from game import collision, lose
from copy import deepcopy
from queue import PriorityQueue


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Agent:
    DIRECTIONS = [[10, 0], [-10, 0], [0, 10], [0, -10]]
    current_path = []

    @staticmethod
    def manhattenDistance(snake_position: tuple[int, int], apple_position: tuple[int, int]) -> int:
        """ Return the distance based in Manhatten calc. """
        return abs(snake_position[0] - apple_position[0]) + abs(
            snake_position[1] - apple_position[1]
        )

    @staticmethod
    def reconstructPath(came_from: dict, current: tuple[int, int]) -> list[tuple[int, int]]:
        """ Will return an array containing the optimal path """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path

    @staticmethod
    def getNeighbors(snake: tuple[list[int]], current: tuple[int, int], border: tuple[list[int]], display_range: int) -> list[tuple[int, int]]:
        """ Return a list with the neighbors """
        neighbors = [
            (
                current[0] + Agent.DIRECTIONS[i][0],
                current[1] + Agent.DIRECTIONS[i][1],
            )
            for i in range(4)
        ]
        neighbors_duplicate = deepcopy(neighbors)
        for i, neighbor in enumerate(neighbors):
            if (
                neighbor[0] < 0
                or neighbor[0] > (display_range - 10)
                or neighbor[1] < 0
                or neighbor[1] > (display_range - 10)
            ):
                neighbors_duplicate.remove(neighbors[i])
            if lose(list(neighbors[i]), snake, border):
                neighbors_duplicate.remove(neighbors[i])
        return neighbors_duplicate

    @staticmethod
    def aStar(snake: tuple[list[int]], apple: tuple[int, int], border: tuple[list[int]], display_range: int, snake_direction: int) -> list[tuple[int, int]]:
        """ Return the path from reconstruct_path method """
        start = snake[0][0], snake[0][1]
        end = apple[0], apple[1]
        count = 0
        priority_queue = PriorityQueue()
        priority_queue.put((0, count, start))
        came_from = {}
        g_score = {}
        g_score[start] = 0
        f_score = {}
        f_score[start] = Agent.manhattenDistance(start, end)
        open_set = {start}
        while not priority_queue.empty():
            current = priority_queue.get()[2]
            open_set.remove(current)
            if collision(current, apple):
                return Agent.reconstructPath(came_from, current)
            neighbors = Agent.getNeighbors(snake, start, border, display_range)
            for neighbor in neighbors:
                if neighbor not in g_score:
                    g_score[neighbor] = math.inf
                    f_score[neighbor] = math.inf
                tentative_g_score = g_score[current]
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + Agent.manhattenDistance(
                        neighbor, end
                    )
                    if neighbor not in open_set:
                        count += 1
                        priority_queue.put(
                            (f_score[neighbor], count, neighbor))
                        open_set.add(neighbor)
                for neighbor in neighbors:
                    neighbors = Agent.getNeighbors(
                        snake, start, border, display_range)
        return []

    @staticmethod
    def verifyDirection(snake_direction_int: int = 0, snake_direction: list[int] = [0, 0]) -> tuple[int, list[int]]:
        """ Verify and transform the direction """
        if snake_direction == [0, -10]:
            snake_direction_int = UP
        elif snake_direction == [0, 10]:
            snake_direction_int = DOWN
        elif snake_direction == [10, 0]:
            snake_direction_int = RIGHT
        elif snake_direction == [-10, 0]:
            snake_direction_int = LEFT
        return snake_direction_int, snake_direction

    @staticmethod
    def makeDecision(snake: tuple[list[int]], apple: tuple[int, int], snake_new_direction: int, border: tuple[list[int]], display_range: int) -> int:
        """
        A star algorithm implementation
        f(n) = g(n) + h(n)
        """
        snake_new_direction, snake_new_direction_list = Agent.verifyDirection(
            snake_new_direction)
        head = snake[0]
        neighbors = [
            (
                head[0] + Agent.DIRECTIONS[i][0],
                head[1] + Agent.DIRECTIONS[i][1],
            )
            for i in range(4)
        ]
        try:
            if not len(Agent.current_path):
                Agent.current_path = Agent.aStar(
                    snake, apple, border, display_range, snake_new_direction)
            try:
                for i, neighbor in enumerate(neighbors):
                    if neighbor == Agent.current_path[-1]:
                        snake_new_direction_list = Agent.DIRECTIONS[i]
                        Agent.current_path.clear()
                        break
            except Exception:
                pass
        except Exception:
            pass
        if not len(Agent.current_path) or len(Agent.current_path) > 1:
            direction = snake_new_direction_list
            distance = math.inf
            for i, path in enumerate(neighbors):
                if Agent.manhattenDistance(path, (apple[0], apple[1])) < distance:
                    if lose(list(path), snake, border):
                        continue
                    direction = Agent.DIRECTIONS[i]
                    distance = Agent.manhattenDistance(
                        path, (apple[0], apple[1]))
            snake_direction, unused = Agent.verifyDirection(0, direction)
            if snake_direction == None:
                return snake_new_direction
            else:
                snake_new_direction = snake_direction
        return snake_new_direction
