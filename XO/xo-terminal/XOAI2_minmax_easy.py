from arabic_reshaper import reshape
from bidi.algorithm import get_display
import random


def pr(text):
    text = reshape(text)
    text = get_display(text)
    return text

#=============================================================================================================
#لیست بازی
board = [['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']]

winer = 0
losser = 0
draw = 0

#چاپ صفجه بازی
def print_board():
    print(' ', 1, 2, 3, sep='  ')
    print(1, board[0][0], board[0][1], board[0][2],sep='  ')
    print(2, board[1][0], board[1][1], board[1][2],sep='  ')
    print(3, board[2][0], board[2][1], board[2][2],sep='  ')

#=============================================================================================================
#برسی برد
def win(W = 'X'):
    #برسی ردیف ها
    if [W, W, W] in board:
        return True

    # برسی ستون‌ها 
    for i in range(3): 
        if board[0][i] == board[1][i] == board[2][i] == W: 
 
            return True

    # برسی قطرها 
    if board[0][0] == board[1][1] == board[2][2] == W or board[0][2] == board[1][1] == board[2][0] == W: 
        return True
    
    return False
    
#برسی تساوی
def is_draw():
    for i in board:
        if '-' in i:
            return False
    return True

#=============================================================================================================
#ورودی کاربر
def entry():
    while True:
        try:
            r = int(input(pr('ردیف:\n')))
            if r<=0 or r>3:
                raise Exception("out renge")
            
            s = int(input(pr('ستون:\n')))
            if s<=0 or s>3:
                raise Exception("out renge")

            
            if board[r-1][s-1] == 'O' or board[r-1][s-1] == 'X':
                print(pr('قبلا انتخاب شده یکی دیگر انتخاب کن'))
                print_board()
                continue
            else:
                board[r-1][s-1] ='X'
                break

        except:
            print(pr('از عدد 1 تا 3 برای انتخاب ردیف و ستون استفاده کن.'))
            print_board()

#=============================================================================================================
# هوش کامپیوتر
def minmax(board, depth, is_maximizing, max_depth):
    if win('O'):
        return 1
    if win('X'):
        return -1
    if is_draw():
        return 0

    if depth >= max_depth:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'O'
                    score = minmax(board, depth + 1, False, max_depth)
                    board[i][j] = '-'
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'X'
                    score = minmax(board, depth + 1, True, max_depth)
                    board[i][j] = '-'
                    best_score = min(score, best_score)
        return best_score

def computer_smart(max_depth=2, random_factor=0.1): #اگر رندوم فاکتور 0 باشد و ماکسیموم دف بی نهایت مین ماکس حداکثر قدرت را دارد
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                if random.random() < random_factor:
                    move = (i, j)
                    break
                board[i][j] = 'O'
                score = minmax(board, 0, False, max_depth)
                board[i][j] = '-'
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = 'O'

#=============================================================================================================
running = True

#حلقه اصلی بازی
while True:
    print_board()

    while running:
        #انتخاب کاربر
        entry()

        #برسی برد یا تساوی کاربر
        if win():
            winer +=1
            print_board()
            print('♦'*10, pr('بردی'),'♦'*10)
            running = False

        if is_draw():
            draw += 1
            print_board()
            print('♦'*10, pr('بازی مساوی شد'), '♦'*10)
            running = False

        if not running:
            break

        #انتخاب کامپیوتر
        computer_smart()
        
        #برسی باخت یا تساوی کاربر
        if win('O'):
            losser += 1
            print_board()
            print('♦'*10, pr('باختی'),'♦'*10)
            running = False

        if is_draw():
            draw += 1
            print_board()
            print('♦'*10, pr('بازی مساوی شد'), '♦'*10)
            running = False

        if not running:
            break

        print_board()

    new = int(input(pr('برای شروع دوباره عدد 1 و برای خروج عدد 2 را وارد کنید.\n')))
    if new == 1:
        board = [['-', '-', '-'],
                ['-', '-', '-'],
                ['-', '-', '-']]
        running = True
    else:
        print(pr(f'برد = {winer} و باخت = {losser} و تساوی = {draw}'))
        break