import pygame as pg
import random, sys

# شروع بازی
pg.init()
pg.font.init()  # مقداردهی اولیه فونت

# تنظیمات رنگ‌ها
background = (30, 30, 30)
green = (0, 255, 0)
red = (225, 0, 0)
white = (255, 255, 255)

# صفحه بازی
screen = pg.display.set_mode((800, 600), pg.RESIZABLE)
pg.display.set_caption('Snake Game')

# اندازه صفحه
wh_pos = (800, 600)
def wh(event_w, event_h):
    global wh_pos
    wh_pos = (event_w, event_h)

# مار
block_size = 10  # اندازه بلوک‌های مار
gap = 3  # فاصله بلوک‌ها

movement = None

# موقعیت اولیه مار
snake_init0 = (random.randint(0, wh_pos[0] - block_size),
               random.randint(0, wh_pos[1] - block_size))
snake_list = [snake_init0]

# امتیاز
score = 0
font = pg.font.SysFont('Arial', 24)

# وضعیت بازی
running = True
game_over = False

# جایزه
gift_EVENT = pg.USEREVENT + 1
pg.time.set_timer(gift_EVENT, 8000)

gift_pos = None  # موقعیت جایزه در ابتدا نامشخص است
gift_size = 20

def new_gift():
    while True:
        gift = (random.randint(0, wh_pos[0] - block_size),
                random.randint(0, wh_pos[1] - block_size))
        if gift not in snake_list:
            return gift

gift_pos = new_gift()  # ایجاد اولین جایزه بلافاصله

# تنظیمات زمان
clock = pg.time.Clock()

while running:

    for event in pg.event.get():

        # بستن بازی
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # اندازه صفحه
        if event.type == pg.VIDEORESIZE:
            screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            wh(event_w=event.w, event_h=event.h)

        if event.type == gift_EVENT:
            gift_pos = new_gift()

        if not game_over:
            # دکمه‌ها
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_UP or event.key == pg.K_w:
                    if movement != 'DOWN':  # جلوگیری از حرکت به جهت مخالف
                        movement = 'UP'
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    if movement != 'UP':
                        movement = 'DOWN'
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    if movement != 'LEFT':
                        movement = 'RIGHT'
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    if movement != 'RIGHT':
                        movement = 'LEFT'

            elif event.type == pg.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = event.pos
                x_head, y_head = snake_list[-1]
                dx = x_mouse - x_head
                dy = y_mouse - y_head

                if abs(dx) > abs(dy):
                    if dx > 0 and movement != 'LEFT':
                        movement = 'RIGHT'
                    elif dx < 0 and movement != 'RIGHT':
                        movement = 'LEFT'
                else:
                    if dy > 0 and movement != 'UP':
                        movement = 'DOWN'
                    elif dy < 0 and movement != 'DOWN':
                        movement = 'UP'
        else:
            # رویدادهای پس از باخت
            if event.type == pg.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = event.pos
                # بررسی کلیک روی دکمه ریست
                if reset_button.collidepoint(x_mouse, y_mouse):
                    # ریست کردن بازی
                    snake_list = [snake_init0]
                    movement = None
                    gift_pos = new_gift()
                    score = 0
                    game_over = False

    if not game_over:
        # حرکت مار در هر فریم
        x_head, y_head = snake_list[-1]
        if movement == 'UP':
            new_head = (x_head, y_head - gap)
        elif movement == 'DOWN':
            new_head = (x_head, y_head + gap)
        elif movement == 'LEFT':
            new_head = (x_head - gap, y_head)
        elif movement == 'RIGHT':
            new_head = (x_head + gap, y_head)
        else:
            new_head = snake_list[-1]  # اگر حرکتی تعیین نشده باشد، موقعیت ثابت می‌ماند

        if movement:
            if new_head in snake_list:
                game_over = True
            else:
                snake_list.append(new_head)
                if gift_pos:
                    snake_rect = pg.Rect(new_head[0], new_head[1], block_size, block_size)
                    gift_rect = pg.Rect(gift_pos[0], gift_pos[1], gift_size, gift_size)

                    if snake_rect.colliderect(gift_rect):
                        gift_pos = new_gift()
                        score += 1  # افزایش امتیاز
                    else:
                        snake_list.pop(0)  # حذف دم مار برای حفظ طول ثابت

                # برخورد با لبه‌ها
                if new_head[0] < 0 or new_head[0] > wh_pos[0] - block_size:
                    game_over = True
                elif new_head[1] < 0 or new_head[1] > wh_pos[1] - block_size:
                    game_over = True

    # رسم صفحه
    screen.fill(background)

    # رسم مار
    for i in range(len(snake_list)):
        pg.draw.rect(screen, green, (*snake_list[i], block_size, block_size))

    # رسم جایزه
    if gift_pos:
        pg.draw.rect(screen, red, (*gift_pos, gift_size, gift_size))

    # نمایش امتیاز
    score_text = font.render(f"score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    if game_over:
        # نمایش پیام باخت
        game_over_text = font.render("You lost.!", True, white)
        text_rect = game_over_text.get_rect(center=(wh_pos[0] / 2, wh_pos[1] / 2 - 50))
        screen.blit(game_over_text, text_rect)

        # رسم دکمه ریست
        reset_button = pg.Rect(wh_pos[0] / 2 - 50, wh_pos[1] / 2, 100, 50)
        pg.draw.rect(screen, white, reset_button)
        reset_text = font.render("restart", True, background)
        reset_text_rect = reset_text.get_rect(center=reset_button.center)
        screen.blit(reset_text, reset_text_rect)

    # تازه‌سازی صفحه
    pg.display.update()
    clock.tick(60)  # تنظیم سرعت بازی