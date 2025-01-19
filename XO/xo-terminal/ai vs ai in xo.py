from random import choice

board = [['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']]

def print_board():
    print(' ', 1, 2, 3, sep='  ')
    print(1, board[0][0], board[0][1], board[0][2],sep='  ')
    print(2, board[1][0], board[1][1], board[1][2],sep='  ')
    print(3, board[2][0], board[2][1], board[2][2],sep='  ')

###################################################

def win(w="X"):
    for row in board:
        if row == [w, w, w]:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == w:
            return True
    if board[0][0] == board[1][1] == board[2][2] == w or board[0][2] == board[1][1] == board[2][0] == w:
        return True
    return False

def draw():
    for row in board:
        if "-" in row:
            return False
    return True

###################################################

def minmax(turn, board, depth, is_maximizing):
    if turn == "O":
        not_turn = "X"
    elif turn == "X":
        not_turn = "O"

    if win(turn):
        return 1
    if win(not_turn):
        return -1
    if draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = turn
                    score = minmax(turn, board, depth + 1, False)
                    board[i][j] = '-'
                    best_score = max(score, best_score)
        return best_score

    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = not_turn
                    score = minmax(turn, board, depth + 1, True)
                    board[i][j] = '-'
                    best_score = min(score, best_score)
        return best_score

def computer_smart_choice(turn):
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = turn
                score = minmax(turn, board, 0, False)
                board[i][j] = '-'
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = turn

###################################################

turn = "X"  # X always starts

while True:
    print_board()
    print("-"*20)

    computer_smart_choice(turn)
    
    if win(turn):
        print_board()
        print(f"{turn} winnaar")
        break
    if draw():
        print_board()
        print("draw")
        break
    
    turn = "O" if turn == "X" else "X"  # Switch turns between X and O