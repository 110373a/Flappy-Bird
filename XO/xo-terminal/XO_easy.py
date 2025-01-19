import random
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def pr(text):
    text = reshape(text)
    text = get_display(text)
    return text

#=============================================================================================================
#لیست بازی
board = [['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']]

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
#هوش کامپیوتر
def computer_smart():
    #تلاش برای برد کامپیوتر
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = 'O'
                if win('O'):
                    return
                board[i][j] = '-'

    #جلوگیری از برد کاربر
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                board[i][j] = 'X'
                if win('X'):
                    board[i][j] = 'O'
                    return
                board[i][j] = '-'

    #انتخاب تصادفی کامپیوتر
    while True:
        random_1 = random.choice(range(3))
        random_2 = random.choice(range(3))
        if board[random_1][random_2] == '-':
            board[random_1][random_2] = 'O'
            break

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
            print_board()
            print('♦'*10, pr('بردی'),'♦'*10)
            running = False

        if is_draw():
            print_board()
            print('♦'*10, pr('بازی مساوی شد'), '♦'*10)
            running = False

        if not running:
            break

        #انتخاب کامپیوتر
        computer_smart()
        
        #برسی باخت یا تساوی کاربر
        if win('O'):
            print_board()
            print('♦'*10, pr('باختی'),'♦'*10)
            running = False

        if is_draw():
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
        break