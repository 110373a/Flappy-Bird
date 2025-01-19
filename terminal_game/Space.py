import random
import time
import curses
stdscr = curses.initscr()     

curses.noecho() #کلیدی رو که می نویسم چاپ نکن
curses.cbreak() #برای انجام کار منتظر اینتر نمون
stdscr.keypad(True)
stdscr.nodelay(True) #منتطر کلید ما نباش
curses.curs_set(False) # پنهان کردن نشان‌گر تایپ

maxl = curses.LINES -1
maxc = curses.COLS -1

world = []
player_c = player_l = 0
food = []
enemy = []
score = 0

# setting
food_age = 100
food_nomber = 10
enemy_number = 3
player_Character = "✈"
food_Character = "☘"
enemy_Character = "☠"

def random_place():
    a = random.randint(0, maxl)
    b = random.randint(0, maxc)
    while world[a][b] != ' ':
        a = random.randint(0, maxl)
        b = random.randint(0, maxc)
    return a,b

def init():
    global player_c, player_l

    for i in range(0, maxl+1):
        world.append([])
        for j in range(0, maxc+1):
            world[i].append(" " if random.random()>0.03 else ".")

    for i in range(food_nomber):
        fl, fc = random_place()
        f_age = random.randint(food_age, food_age*10)
        food.append([fl, fc, f_age])

    for i in range(enemy_number):
        el, ec = random_place()
        enemy.append([el, ec])

    player_l, player_c = random_place()

def drow(): 
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i,j,world[i][j])

    stdscr.addstr(1, 1, f"score: {score}")

    for f in food:
        fl, fc, f_age = f
        stdscr.addch(fl, fc, food_Character)

    for e in enemy:
        el, ec = e
        stdscr.addch(el, ec, enemy_Character)

    stdscr.addch(player_l, player_c, player_Character)
    stdscr.refresh()

def in_range(a, min, max):
    if a > max:
        return max
    if a < min:
        return min
    return a

def move():
    global player_l, player_c
    if c == 'w' and world[player_l-1][player_c] != '.':
        player_l -=1
    if c == 's' and world[player_l+1][player_c] != '.':
        player_l +=1
    if c == 'a' and world[player_l][player_c-1] != '.':
        player_c -=1
    if c == 'd' and world[player_l][player_c+1] != '.':
        player_c +=1

    player_l = in_range(player_l, 0, maxl -1)
    player_c = in_range(player_c, 0, maxc -1)

def check_food():
    global score
    for i in range(len(food)):
        fl, fc, f_age = food[i]
        f_age -= 1
        if fl == player_l and fc == player_c:
            score += 10
            fl, fc = random_place()
            f_age = random.randint(food_age, food_age*10)
        if f_age <= 0:
            fl, fc = random_place()
            f_age = random.randint(food_age, food_age*10)
        food[i] = (fl, fc,  f_age)

def move_enemy():
    global playing
    for i in range(len(enemy)):
        el, ec = enemy[i]
        if random.random()>0.8:
            if el > player_l:
                el -= 1
        if random.random()>0.8:
            if ec > player_c:
                ec -= 1
        if random.random()>0.8:
            if el < player_l:
                el += 1
        if random.random()>0.8:
            if ec < player_c:
                ec +=1
            el = in_range(el, 0, maxl -1)
            ec = in_range(ec, 0, maxc -1)
            enemy[i] = (el, ec)
        if el == player_l and ec == player_c:
            stdscr.addstr(maxl//2, maxc//2, "YOU DIED!")
            stdscr.refresh()
            time.sleep(2)
            playing = False

init()
playing = True
while playing:
    try:
        c = stdscr.getkey()
    except:
        c = ''
    if c in "asdw":
        move()
    elif c == 'q':
        playing = False
    check_food()
    move_enemy()
    time.sleep(0.01) # این به جای موو انمی رندوم
    drow()

stdscr.clear()
stdscr.refresh()