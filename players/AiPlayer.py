from players.Player import Player

class AiPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        
    def control(event, direction: int, snake, apple_pos) -> int:
        colli = super().find_possible_collision(snake[0])

        if colli != False and colli == direction:
            return super().redirect(2, direction)

        if snake[0][0] != apple_pos[0]:
            if snake[0][0] > apple_pos[0]:
                return super().LEFT
            if snake[0][0] < apple_pos[0]:
                return super().RIGHT
        if snake[0][1] != apple_pos[1]:
            if snake[0][1] > apple_pos[1]:
                return super().UP
            if snake[0][1] < apple_pos[1]:
                return super().DOWN
        
        return direction
        return redirect(input, direction)
        
