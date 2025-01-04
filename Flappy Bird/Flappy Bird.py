import pygame
import sys
import random

#شروع برنامه
pygame.init()

#متغیر وضعیت بازی
game_status = False

#زمان
clock = pygame.time.Clock()

#صفحه بازی
x = 480
y = 850
main_screen = pygame.display.set_mode((x, y))

#بکگراند
background_image = pygame.transform.scale2x(pygame.image.load(r"assets\img\bg1.png"))

#زمین بازی
floor_image = pygame.transform.scale2x(pygame.image.load(r"assets\img\floor.png"))
floor_x = 0

#=================================================================================================================
#صدا ها
win_sound = pygame.mixer.Sound(r"assets\sound\smb_stomp.wav")
game_over_sound = pygame.mixer.Sound(r"assets\sound\smb_mariodie.wav")

#=================================================================================================================
#امتیازدهی
game_font = pygame.font.Font(r"assets\font\Flappy.TTF", 40)

#نمایش امتیاز
score = 0
high_score = 0
activee_score = True

def display_score(status):
    if status == 'active':
        text_score = game_font.render(str(score), False, (255,255,255)) 
        text_score_rect = text_score.get_rect(center = (240, 60))
        main_screen.blit(text_score, text_score_rect)
    
    if status == 'game_over':
        text_score = game_font.render(f'Score: {score}', False, (255,255,255)) 
        text_score_rect = text_score.get_rect(center = (240, 60))
        main_screen.blit(text_score, text_score_rect)

        text_high = game_font.render(f'High Score: {high_score}', False, (255,255,255)) 
        text_high_rect = text_high.get_rect(center = (240, 680))
        main_screen.blit(text_high, text_high_rect)

#آبدیت امتیاز
def update_score():
    global score, high_score, activee_score
    if pipe_list:
        for pipe in pipe_list:
            if 75 < pipe.centerx < 85 and activee_score:
                win_sound.play()
                score += 1
                activee_score = False
            if pipe.centerx < 0:
                activee_score = True

    if score > high_score:
        high_score = score
    return high_score

#=================================================================================================================
#لوله ها
pipe_image = pygame.transform.scale2x(pygame.image.load(r"assets\img\pipe_green.png"))
create_pipe = pygame.USEREVENT
pygame.time.set_timer(create_pipe, 1400)
pipe_list = []

#تابع ساخت لوله
def generate_pipe_rect():
    random_pipe = random.randrange(280, 650)
    pipe_rect_top = pipe_image.get_rect(midbottom = (500, random_pipe - 200))
    pipe_rect_bottom = pipe_image.get_rect(midtop = (500, random_pipe))
    return pipe_rect_top , pipe_rect_bottom

#تابع حرکت لوله
def move_pipe_rect(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    inside_pipe = [pipe for pipe in pipes if pipe.right > -20]
    return inside_pipe

#تابع نمایش لوله
def display_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 850:
            main_screen.blit(pipe_image, pipe)
        else:
            main_screen.blit(pygame.transform.flip(pipe_image, False, True), pipe)

#=================================================================================================================
#پرنده
bird_mid_image = pygame.transform.scale2x(pygame.image.load(r"assets\img\red_bird_mid_flap.png"))
bird_up_image = pygame.transform.scale2x(pygame.image.load(r"assets\img\red_bird_up_flap.png"))
bird_down_image = pygame.transform.scale2x(pygame.image.load(r"assets\img\red_bird_down_flap.png"))

#نمایش پرواز پرنده
bird_list_index = 0
bird_list = [bird_down_image, bird_mid_image, bird_up_image]
bird_image = bird_list[bird_list_index]

create_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_flap, 100)
def bird_animition():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center = (80, bird_image_rect.centery))
    return new_bird, new_bird_rect

bird_image_rect = bird_image.get_rect(center = (80, 0))
Gravity = 0.20
bird_movment =0 
#=================================================================================================================
#صفحه شروع و باخت
start_image = pygame.transform.scale2x(pygame.image.load(r"assets\img\message.png"))
start_image_rect = start_image.get_rect(center = (240, 370))

#تابع برخورد پرنده به لوله
def check_collision(pipes):
    global activee_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            activee_score = True
            return False
        if bird_image_rect.top <= -50 or bird_image_rect.bottom >= 730:
            game_over_sound.play()
            return False
    return True

#=================================================================================================================
while True:
    #خروج از برنامه
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            #پایان برنامه
            pygame.quit()
            #خروج از برنامه
            sys.exit()

        #پرش پرنده با دکمه
        if event.type == pygame.KEYDOWN:
            if event.key:
                bird_movment = 0
                bird_movment -= 6
            
            #ریست بازی با دکمه
            if event.key and not game_status:
                game_over_sound.stop()
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (800, 425)
                bird_movment = 0
                score = 0

        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1: 
                bird_movment = 0 
                bird_movment -= 6

            if event.button == 1 and not game_status: 
                game_over_sound.stop()
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (800, 425)
                bird_movment = 0
                score = 0


        #ساخت لوله در ایونت زمان
        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())

        #ساخت پرواز در ایونت زمان
        if event.type == create_flap:
            if bird_list_index < 2:
                bird_list_index +=1
            else:
                bird_list_index = 0
                
            bird_image, bird_image_rect = bird_animition()

    #نمایش بکگراند
    main_screen.blit(background_image, (0, -150))

    # برسی وضعیت برد و باخت
    if game_status:
        # ذخیره وضعیت برد و باخت
        game_status = check_collision(pipe_list)

        #نمایش پرنده
        main_screen.blit(bird_image, bird_image_rect)

        #فراخوانی تابع حرکت لوله
        pipe_list = move_pipe_rect(pipe_list)
        #نمایش لوله
        display_pipe(pipe_list)

        #جاذبه (پایین رفتن پرنده)
        bird_movment += Gravity
        bird_image_rect.centery += bird_movment

        #نمایش امتیاز
        update_score()
        display_score('active')
    else:
        display_score('game_over')
        main_screen.blit(start_image, start_image_rect) 
        
    #حرکت زمین
    main_screen.blit(floor_image, (floor_x, 750))
    main_screen.blit(floor_image, (floor_x+576, 750))
    if floor_x <= -576:
        floor_x = 0
    else:
        floor_x -=1
        
    #تازه سازی یا رفرش ریت
    pygame.display.update()
    clock.tick(90)
