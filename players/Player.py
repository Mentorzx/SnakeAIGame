
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Player():
    def __init__(self) -> None:
        pass
    
    def control(event, direction: int) -> int:
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