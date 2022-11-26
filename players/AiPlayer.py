from players.Player import Player

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class AiPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        
    def control_AI(self, direction, snake, apple_pos):
        colli = super().find_possible_collision(snake[0])

        # if colli != False and colli == direction:
        #     return super().redirect(2, direction) 

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
        
