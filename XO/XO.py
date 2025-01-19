import tkinter as tk
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import random

#####################################################################################
# لیست بازی
board = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]

winer = 0
losser = 0
draw = 0

#####################################################################################
def win(W='X'):
    if [W, W, W] in board:
        return True
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == W:
            return True
    if board[0][0] == board[1][1] == board[2][2] == W or board[0][2] == board[1][1] == board[2][0] == W:
        return True
    return False

def is_draw():
    for i in board:
        if '-' in i:
            return False
    return True

#####################################################################################
# الگوریتم‌های مختلف کامپیوتر
def computer_smart_medium(max_depth=3, random_factor=0):
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
    if move and running:
        board[move[0]][move[1]] = 'O'

def computer_smart_hard():
    computer_smart_medium(max_depth=float('inf'), random_factor=0)

def computer_smart_easy():
    computer_smart_medium(max_depth=2, random_factor=0.4)
#####################################################################################
# الگوریتم Minimax
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

#####################################################################################
running = True

# رابط کاربری
def reset_board():
    global running
    global board
    board = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    status_label.config(text=(' '))
    running = True
    update_board()

def update_board():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=board[i][j])

def handle_click(r, c):
    global winer, losser, draw, running
    if board[r][c] != '-':
        return
    if running:
        board[r][c] = 'X'
    update_board()

    if win():
        if running:
            winer += 1
        status_label.config(text=(" بردی "), foreground="green")
        running = False
        return

    if is_draw():
        if running:
            draw += 1
        status_label.config(text=(" بازی مساوی شد "), foreground="blue")
        running = False
        return

    # انتخاب الگوریتم بر اساس حالت
    selected_mode = mode_var.get()
    if selected_mode == "آسان":
        computer_smart_easy()
    elif selected_mode == "متوسط":
        computer_smart_medium()
    elif selected_mode == "سخت":
        computer_smart_hard()

    update_board()

    if win('O'):
        if running:
            losser += 1
        status_label.config(text=(" باختی "), foreground="red")
        running = False
        return

    if is_draw():
        if running:
            draw += 1
        status_label.config(text=(" بازی مساوی شد "), foreground="blue")
        running = False
        return

#####################################################################################
# تنظیمات پنجره اصلی
root = tk.Tk()
root.title("XO بازی")
root.configure(background="#121212")
root.resizable(False, False)

# متغیر حالت
mode_var = tk.StringVar(value="متوسط")  # حالت پیش‌فرض

# دکمه‌های رادیویی برای انتخاب حالت
tk.Radiobutton(root, text="آسان", variable=mode_var, value="آسان", font=("Arial", 12), background="#121212", foreground="white", selectcolor="black").grid(row=0, column=0)
tk.Radiobutton(root, text="متوسط", variable=mode_var, value="متوسط", font=("Arial", 12), background="#121212", foreground="white", selectcolor="black").grid(row=0, column=1)
tk.Radiobutton(root, text="سخت", variable=mode_var, value="سخت", font=("Arial", 12), background="#121212", foreground="white", selectcolor="black").grid(row=0, column=2)

# دکمه‌های بازی
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='-', font=("Arial", 24), width=5, height=2, foreground="white", background="#696969",
                                command=lambda r=i, c=j: handle_click(r, c))
        buttons[i][j].grid(row=i+1, column=j)

# برچسب وضعیت
status_label = tk.Label(root, text=("None"), font=("Arial", 16), background="#121212", foreground="white")
status_label.grid(row=4, column=0, columnspan=3)

# دکمه شروع دوباره
reset_button = tk.Button(root, text=("شروع دوباره"), font=("Arial", 14), foreground="white", background="#696969", command=reset_board)
reset_button.grid(row=5, column=0, columnspan=3)

#صفحه برد و باخت
def Win_lose_situation():
    global winer, losser, draw
    nroot = tk.Tk()
    nroot.title("تعداد برد و باخت")
    nroot.configure(background="#121212")
    nroot.resizable(False, False)
    #برچسب تعداد برد و باخت
    status_label_status = tk.Label(nroot, text=(''), font=("Arial", 28), background="#121212", foreground="white")
    status_label_status.config(text=(f'برد = {winer}\nتساوی = {draw}\nباخت = {losser}'), foreground="white")
    status_label_status.grid(row=4, column=0, columnspan=3)

#تعداد برد و باخت بازی بازی
reset_button = tk.Button(root, text=("تعداد برد و باخت"), font=("Arial", 14), foreground="white", background="#696969", command=Win_lose_situation)
reset_button.grid(row=10, column=0, columnspan=3)

# اجرای برنامه
reset_board()
root.mainloop()