import pygame
import sys
import random

# شروع بازی
pygame.init()

# مقداردهی اولیه ماژول mixer
pygame.mixer.init()

rock_image = pygame.image.load(r"assets\hands\rock.png")
paper_image = pygame.image.load(r"assets\hands\paper.png")
scisser_image = pygame.image.load(r"assets\hands\scisser.png")

sound = pygame.mixer.Sound(r"assets\sound\jump.wav")

# صفحه بازی
screen = pygame.display.set_mode((600, 400))

# وضعیت اجرای بازی
running = True

# رنگ تصادفی
def get_random_color():
    x = random.randint(1, 255)
    y = random.randint(1, 255)
    z = random.randint(1, 255)
    return (x, y, z)
random_color = get_random_color()

def computer_choice():
    return random.choice(["rock", "paper", "scisser"])

def get_user_choice(mouse_pos):
    if rock_image_rect.collidepoint(mouse_pos):
        return "rock"
    elif paper_image_rect.collidepoint(mouse_pos):
        return "paper"
    elif scisser_image_rect.collidepoint(mouse_pos):
        return "scisser"
    return None

user_choice = None
comp_choice = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            random_color = get_random_color()
            sound.play()
            user_choice = get_user_choice(event.pos)
            if user_choice:
                comp_choice = computer_choice()
            else:
                comp_choice = None

    screen.fill(random_color)

    rock_image_rect = rock_image.get_rect(topleft=(30, 0))
    paper_image_rect = paper_image.get_rect(topleft=(245, 0))
    scisser_image_rect = scisser_image.get_rect(topleft=(430, 0))

    screen.blit(rock_image, rock_image_rect.topleft)
    screen.blit(paper_image, paper_image_rect.topleft)
    screen.blit(scisser_image, scisser_image_rect.topleft)

    if user_choice:
        if user_choice == "rock":
            screen.blit(rock_image, (150, 200))
        elif user_choice == "paper":
            screen.blit(paper_image, (150, 200))
        elif user_choice == "scisser":
            screen.blit(scisser_image, (150, 200))

    if comp_choice:
        if comp_choice == "rock":
            screen.blit(rock_image, (350, 200))
        elif comp_choice == "paper":
            screen.blit(paper_image, (350, 200))
        elif comp_choice == "scisser":
            screen.blit(scisser_image, (350, 200))

    pygame.display.flip()