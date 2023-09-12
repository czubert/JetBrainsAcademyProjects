import random

msg_0 = 'You should enter numbers!'
msg_1 = 'Coordinates should be from 1 to 3!'
msg_2 = 'This cell is occupied! Choose another one!'
msg_3 = 'Bad parameters!'
msg_4 = 'Making move level "easy"'
msg_5 = 'Making move level "medium"'
msg_6 = 'Making move level "hard"'
game_not_finished = 'Game not finished'


def line_to_string(line):
    str_line = ' '.join([' ' if _ == '_' else _ for _ in line])
    return f'| {str_line} |'


def print_lines(lines):
    str_lines = [line_to_string(_) for _ in lines]
    print(f'''{9 * '-'}
{str_lines[0]}
{str_lines[1]}
{str_lines[2]}
{9 * '-'}''')


def check_status(lines):
    for i in range(len(lines)):
        x_in_row = lines[i].count('X')
        x_in_column = [lines[n][i] for n in range(len(lines))].count('X')
        o_in_row = lines[i].count('O')
        o_in_column = [lines[n][i] for n in range(len(lines))].count('O')
        if x_in_row == 3 or x_in_column == 3:
            return 'X wins'
        elif o_in_row == 3 or o_in_column == 3:
            return 'O wins'
    x_diagonal = (lines[0][0] == 'X' and lines[1][1] == 'X' and lines[2][2] == 'X') or (
            lines[2][0] == 'X' and lines[1][1] == 'X' and lines[0][2] == 'X')
    o_diagonal = (lines[0][0] == 'O' and lines[1][1] == 'O' and lines[2][2] == 'O') or (
            lines[2][0] == 'O' and lines[1][1] == 'O' and lines[0][2] == 'O')
    if x_diagonal:
        return 'X wins'
    elif o_diagonal:
        return 'O wins'
    elif any([True for line in lines if line.count('_')]):
        return 'Game not finished'
    return 'Draw'


def enter_coordinates(lines):
    while True:
        coordinates = input('Enter the coordinates: ').split()
        if len(coordinates) != 2:
            print(msg_0)
            continue
        input_x, input_y = coordinates
        try:
            int_x, int_y = int(input_x) - 1, int(input_y) - 1
        except ValueError:
            print(msg_0)
            continue
        if not 0 <= int_x <= 2 or not 0 <= int_y <= 2:
            print(msg_1)
            continue
        elif lines[int_x][int_y] != '_':
            print(msg_2)
            continue
        else:
            break
    return int_x, int_y


def ai_move_easy(lines):
    while True:
        x_ai = random.randint(0, 2)
        y_ai = random.randint(0, 2)
        if lines[x_ai][y_ai] == '_':
            break
    return x_ai, y_ai


def ai_move_medium(lines, ai_symbol, opponent_symbol):
    check1 = check_2_in_line(lines, ai_symbol)
    check2 = check_2_in_line(lines, opponent_symbol)
    if check1[0]:
        x_ai, y_ai = check1[1], check1[2]
    elif check2[0]:
        x_ai, y_ai = check2[1], check2[2]
    else:
        x_ai, y_ai = ai_move_easy(lines)
    return x_ai, y_ai


def check_2_in_line(lines, check_symbol):
    for i in range(len(lines)):
        n = 0
        symbol_in_row = lines[i].count(check_symbol)
        blank_in_row = lines[i].count('_')
        symbol_in_column = [lines[n][i] for n in range(len(lines))].count(check_symbol)
        blank_in_column = [lines[n][i] for n in range(len(lines))].count('_')
        if symbol_in_row == 2 and blank_in_row == 1:
            for x in lines[i]:
                if x == '_':
                    return [True, i, n]
                n += 1
        elif symbol_in_column == 2 and blank_in_column == 1:
            for x in lines:
                if x[i] == '_':
                    return [True, n, i]
                n += 1
    diagonal_1 = [lines[i][i] for i in range(len(lines))]
    diagonal_2 = [lines[i][2 - i] for i in range(len(lines))]
    n = 0
    if diagonal_1.count(check_symbol) == 2 and diagonal_1.count('_') == 1:
        for x in diagonal_1:
            if x == '_':
                return [True, n, n]
            n += 1
    elif diagonal_2.count(check_symbol) == 2 and diagonal_2.count('_') == 1:
        for x in diagonal_2:
            if x == '_':
                return [True, n, 2 - n]
            n += 1
    return [False, 0, 0]


def lines_to_array(lines):
    array = []
    n = 0
    for x in range(len(lines)):
        for y in range(len(lines)):
            if lines[x][y] == 'X' or lines[x][y] == 'O':
                array.append(lines[x][y])
            else:
                array.append(n)
            n += 1
    return array


def minimax(lines, player, step):
    board = lines.copy()
    avail_slots = list(filter(lambda x: x != 'X' and x != 'O', board))

    if step == 'X':
        second_step = 'O'
    else:
        second_step = 'X'

    if winning(board, step):
        return {'score': 10}
    elif winning(board, second_step):
        return {'score': -10}
    elif len(avail_slots) == 0:
        return {'score': 0}

    if player == 'X':
        second_player = 'O'
    else:
        second_player = 'X'
    moves = []

    for i in avail_slots:
        board[i] = player
        move = {'index': i, 'score': minimax(board, second_player, step)['score']}
        board[i] = i
        moves.append(move)

    best_move = 0
    if player == step:
        best_score = -10000
        for i in range(len(moves)):
            if best_score < moves[i]['score']:
                best_score = moves[i]['score']
                best_move = i
    else:
        best_score = 10000
        for i in range(len(moves)):
            if best_score > moves[i]['score']:
                best_score = moves[i]['score']
                best_move = i
    result = moves[best_move]
    return result


def winning(table, checked_symbol):
    if table[0] == checked_symbol and table[1] == checked_symbol and table[2] == checked_symbol or \
            table[3] == checked_symbol and table[4] == checked_symbol and table[5] == checked_symbol or \
            table[6] == checked_symbol and table[7] == checked_symbol and table[8] == checked_symbol or \
            table[0] == checked_symbol and table[3] == checked_symbol and table[6] == checked_symbol or \
            table[1] == checked_symbol and table[4] == checked_symbol and table[7] == checked_symbol or \
            table[2] == checked_symbol and table[5] == checked_symbol and table[8] == checked_symbol or \
            table[0] == checked_symbol and table[4] == checked_symbol and table[8] == checked_symbol or \
            table[2] == checked_symbol and table[4] == checked_symbol and table[6] == checked_symbol:
        return True
    else:
        return False


def ai_move_hard(n):
    x = n // 3
    y = n % 3
    return x, y


def start_game():
    # Start game board
    start = list('_________')
    # Create nested list from input data
    game_board = [start[:3], start[3:6], start[6:]]
    # Define player symbol
    player1_symbol, player2_symbol = 'X', 'O'
    return game_board, player1_symbol, player2_symbol


def player_move(game_board, player, player_symbol, opponent_symbol):
    print_lines(game_board)
    if player == 'user':
        x, y = enter_coordinates(game_board)
    elif player == 'easy':
        x, y = ai_move_easy(game_board)
        print(msg_4)
    elif player == 'medium':
        x, y = ai_move_medium(game_board, player_symbol, opponent_symbol)
        print(msg_5)
    else:
        game_board_array = lines_to_array(game_board)
        number = minimax(game_board_array, player_symbol, player_symbol)['index']
        x, y = ai_move_hard(number)
        print(msg_6)
    game_board[x][y] = player_symbol
    return game_board


def game(game_board, player_1, player_2, player1_symbol, player2_symbol):
    while True:
        game_board = player_move(game_board, player_1, player1_symbol, player2_symbol)
        if check_status(game_board) != game_not_finished:
            break
        game_board = player_move(game_board, player_2, player2_symbol, player1_symbol)
        if check_status(game_board) != game_not_finished:
            break
    print_lines(game_board)
    return check_status(game_board)


def main():
    while True:
        cmd = input('Input command: ').split(' ')
        if cmd[0] == 'exit':
            break
        elif cmd[0] == 'start' and len(cmd) == 3:
            board, symbol_player_x, symbol_player_o = start_game()
            status = game(board, cmd[1], cmd[2], symbol_player_x, symbol_player_o)
            print(status)
        else:
            print(msg_3)
            continue


if __name__ == '__main__':
    main()
