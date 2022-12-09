from ctypes import windll
import game

def read_move_file(save_number: str) -> str:
    """ Read the record file """
    with open('save.txt', 'r') as save_file:
        lines = save_file.readlines()
    line = 0
    while lines[line] != f'save_number: {save_number}':
        line += 1
    return lines[line + 1]


def startRecord(display_range: int, start_snake: tuple[list[int]]) -> str:
    """ Make the header of the record file """
    # region Get record number
    with open('config.txt', 'r') as config_file:
        record_number = config_file.readline().strip().split(' ')[1]
    with open('config.txt', 'w') as config_file:
        config_file.write(f'record_number: {int(record_number) + 1}')
    # endregion

    record = f'Save: {record_number} \n'
    record += f'Display_range: {display_range} \n'

    record += f'Start_position: '
    for gomo in start_snake:
        record += f'[{gomo[0]},{gomo[1]}]-'
    record += f'\n'
    return record


def finishRecord(record: str, time_in_game: str) -> None:
    """ Make the end of the record giving some space for the next one """
    with open('save.txt', 'a') as record_file:
        record_file.write(f'{record} DEATH \n')
        record_file.write(f'Time: {time_in_game}\n\n')


def recordMoveFormat(direction: int, apple_pos: tuple[int, int]) -> str:
    """ Return the informations on file format """
    return f'({direction},{apple_pos[0]},{apple_pos[1]})-'


def recordReadMoveFormat(move: str) -> tuple[int, tuple[int, int]]:
    """ Return the information inscribed in the string """
    direction, apple_pos_X, apple_pos_Y = map(int, move.strip().replace('(', '').replace(')', '').split(','))
    apple = tuple((apple_pos_X, apple_pos_Y))
    return direction, tuple(apple)


def recordReadStart(playback_number: int) -> tuple[int, tuple[list[int]], list[str]]:
    """ Return the start conditions/information from the specified record """
    with open('save.txt', 'r') as record_file:
        while True:
            line = record_file.readline().strip().split(' ')
            if line[0].__contains__('Save') and int(line[1]) == playback_number:
                break

        display_range = int(record_file.readline().strip().split(' ')[1])

        snake_str = record_file.readline().strip().split(' ')[1].split('-')
        snake = []
        for i, gomo in enumerate(snake_str):
            if not gomo:
                break
            gomo_X, gomo_Y = map(int, gomo.strip().replace('[', '').replace(']', '').split(','))
            snake.append((gomo_X, gomo_Y))

        moves = record_file.readline().strip().split('-')

    return display_range, tuple(snake), moves


def finishPlayback(snake: tuple[list[int]], display_range: int, border: tuple[list[int]], score: int, start_time: int) -> None:
    """ End of the playback """
    decision = 0
    MessageBox = windll.user32.MessageBoxW
    if game.win(snake, display_range) or game.lose(list(snake)[0], tuple(snake), border):
        decision = MessageBox(
            None, f'End of record!!! Score: {score}.', f'Game Over in {game.timeinGame(start_time)} minutes.', 5)
    if decision == 2:
        quit()
        exit()