import pygame
import random
import sys
import time
import math

# for music
pygame.init()
pygame.mixer.init()

# snake colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 102, 204)
d_green = (1, 162, 0)
yellow = (255, 255, 0)

soundtrack = pygame.mixer_music

# play music or not
on_off = True

dis_width = 600
dis_height = 400

# display - frame

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake")  # name of the game

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

# fonts of different text
font_style = pygame.font.SysFont("rockout", 30)
score_font = pygame.font.SysFont("rockout", 30)
font_menu = pygame.font.SysFont('rockout', 26)

# snake color
color_list = [green, blue, yellow, white]

number_for_color = 0
number_of_games = 0

# show your score - top left corner


def your_score(score):
    global value
    value = score_font.render("Your score: " + str(score), True, white)
    dis.blit(value, [0, 0])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 8 - 50, dis_height / 3])


def game():
    game_over = False
    game_close = False

    # initial coordinates
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # random spawn of food

    foodx = round(random.randrange(0, dis_width - snake_block) / 15.0) * 10.0
    foody = round(random.randrange(0, dis_width - snake_block) / 15.0) * 10.0

    food = []
    food.append(foodx)
    food.append(foody)


    while not game_over:
        while game_close is True:

            time.sleep(1)
            dis.fill(black)
            message("You Lost! Press ESC-Main menu or SPACE-Play Again", white)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        dis.fill(main_menu())

                    elif event.key == pygame.K_SPACE:
                        game()

    # mouse and button control

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # snake movement

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            if on_off is True:
                pygame.mixer_music.load('game_over.mp3')
                pygame.mixer_music.play(0)
            game_close = True

        x1 += x1_change
        y1 += y1_change

        # backround

        dis.fill(black)

        # food
        if food not in snake_List:
            pygame.draw.rect(dis, color_list[number_for_color], [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # if snake crash into borders - turn snake red
        for x in snake_List:
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])
            else:
                pygame.draw.rect(dis, color_list[number_for_color], [x[0], x[1], snake_block, snake_block])

        for x in snake_List[:-1]:
            if x == snake_Head:
                for j in snake_List:
                    pygame.draw.rect(dis, red, [j[0], j[1], snake_block, snake_block])

                if on_off is True:
                    pygame.mixer_music.load('game_over.mp3')
                    pygame.mixer_music.play(0)

                game_close = True

        your_score(Length_of_snake - 1)
        pygame.display.update()

        # if snake eats the food, make new block of food
        if x1 == foodx and y1 == foody:
            if on_off is True:
                pygame.mixer_music.load('food.mp3')
                pygame.mixer_music.play(0)

            foodx = round(random.randrange(0, dis_width - snake_block) / 15.0) * 10.0
            foody = round(random.randrange(0, dis_width - snake_block) / 15.0) * 10.0
            Length_of_snake += 1
            food = []

        while foodx and foody in snake_List:
            food = []
            foodx = round(random.randrange(0, dis_width - snake_block) / 15.0) * 10.0
            foody = round(random.randrange(0, dis_width - snake_block) / 15.0) * 10.0
            food.append(foodx)
            food.append(foody)

        clock.tick(snake_speed)

    pygame.quit()
    quit()


# arrows displayed in settings

def draw_arrow_up(screen, start, end):
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 180
    pygame.draw.polygon(screen, white, (
        (end[0] + 10 * math.sin(math.radians(rotation)), end[1] + 10 * math.cos(math.radians(rotation))),
        (end[0] + 10 * math.sin(math.radians(rotation - 120)), end[1] + 10 * math.cos(math.radians(rotation - 120))),
        (end[0] + 10 * math.sin(math.radians(rotation + 120)), end[1] + 10 * math.cos(math.radians(rotation + 120)))),
                        1)


def draw_arrow_down(screen, start, end):
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0]))
    pygame.draw.polygon(screen, white, (
        (end[0] + 10 * math.sin(math.radians(rotation)), end[1] + 10 * math.cos(math.radians(rotation))),
        (end[0] + 10 * math.sin(math.radians(rotation - 120)), end[1] + 10 * math.cos(math.radians(rotation - 120))),
        (end[0] + 10 * math.sin(math.radians(rotation + 120)), end[1] + 10 * math.cos(math.radians(rotation + 120)))),
                        1)


def draw_arrow_left(screen, color, start, end):
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 270
    pygame.draw.polygon(screen, color, (
        (end[0] + 10 * math.sin(math.radians(rotation)), end[1] + 10 * math.cos(math.radians(rotation))),
        (end[0] + 10 * math.sin(math.radians(rotation - 120)), end[1] + 10 * math.cos(math.radians(rotation - 120))),
        (end[0] + 10 * math.sin(math.radians(rotation + 120)), end[1] + 10 * math.cos(math.radians(rotation + 120)))),
                        1)


def draw_arrow_right(screen, color, start, end):
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(screen, color, (
        (end[0] + 10 * math.sin(math.radians(rotation)), end[1] + 10 * math.cos(math.radians(rotation))),
        (end[0] + 10 * math.sin(math.radians(rotation - 120)), end[1] + 10 * math.cos(math.radians(rotation - 120))),
        (end[0] + 10 * math.sin(math.radians(rotation + 120)), end[1] + 10 * math.cos(math.radians(rotation + 120)))),
                        1)

# draw an actual snake


def draw_snake(screen):
    global number_for_color
    x = 337
    y = 267

    if number_for_color == len(color_list) or number_for_color == -4:
        number_for_color = 0
    for i in range(5):
        s_snake = pygame.Rect(x, y, 15, 15)
        pygame.draw.rect(screen, color_list[number_for_color], s_snake)
        x += 15


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False

# settings for option "settings"


def settings():
    global click, on_off, number_for_color

    click = False
    on_off = True
    running = True

    while running:

        dis.fill(black)

        draw_text('Settings', font_style, white, dis, 250, 80)
        draw_text('Movements', font_menu, white, dis, 173, 166)
        draw_text('Music', font_menu, white, dis, 195, 216)
        draw_text('Snake color', font_menu, white, dis, 172, 265)

        mx, my = pygame.mouse.get_pos()
        move = pygame.Rect(dis_height / 2 - 45, dis_width / 2 - 140, dis_height / 2 - 70, dis_width / 2 - 270)
        sound = pygame.Rect(dis_height / 2 - 45, dis_width / 2 - 90, dis_height / 2 - 70, dis_width / 2 - 270)
        s_color = pygame.Rect(dis_height / 2 - 45, dis_width / 2 - 40, dis_height / 2 - 70, dis_width / 2 - 270)

        sound_on = pygame.Rect(dis_height / 2 + 101, dis_width / 2 - 90, dis_height / 2 - 150, dis_width / 2 - 270)
        sound_off = pygame.Rect(dis_height / 2 + 151, dis_width / 2 - 90, dis_height / 2 - 150, dis_width / 2 - 270)

        left_arrow_click = pygame.Rect(305, 265, 15, 20)
        right_arrow_click = pygame.Rect(430, 265, 16, 20)

        pygame.draw.rect(dis, white, sound_on, 1)
        pygame.draw.rect(dis, white, sound_off, 1)
        pygame.draw.rect(dis, black, left_arrow_click)
        pygame.draw.rect(dis, black, right_arrow_click)

        draw_arrow_left(dis, d_green, (310, 275), (315, 275))
        draw_arrow_right(dis, d_green, (430, 275), (435, 275))

        if sound_off.collidepoint((mx, my)):
            if click:
                on_off = False
            pygame.draw.rect(dis, red, sound_off)

        if sound_on.collidepoint((mx, my)):
            if click:
                on_off = True

            pygame.draw.rect(dis, blue, sound_on)

        if left_arrow_click.collidepoint((mx, my)):
            if click:
                number_for_color -= 1

        if right_arrow_click.collidepoint((mx, my)):
            if click:
                number_for_color += 1

        draw_snake(dis)

        pygame.draw.rect(dis, d_green, move, 1)  # outline - 1
        pygame.draw.rect(dis, d_green, sound, 1)
        pygame.draw.rect(dis, d_green, s_color, 1)

        draw_arrow_up(dis, (310, 155), (351, 155))
        draw_arrow_down(dis, (310, 184), (351, 184))
        draw_arrow_left(dis, white, (325, 170), (330, 170))
        draw_arrow_right(dis, white, (360, 170), (370, 170))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = True

        draw_text('On', font_menu, white, dis, 313, 216)
        draw_text('Off', font_menu, white, dis, 362, 216)

        pygame.display.flip()

        pygame.display.update()
        clock.tick(60)

# settings for "main menu"


def main_menu():
    global click
    global on_off

    running1 = True

    while running1:
        dis.fill(black)
        draw_text('Main menu', font_style, white, dis, 240, 80)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(219, 158, 151, 32)
        button_2 = pygame.Rect(219, 223, 151, 32)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
                running1 = False
            pygame.draw.rect(dis, d_green, button_1)

        if button_2.collidepoint((mx, my)):
            if click:
                settings()
            pygame.draw.rect(dis, d_green, button_2)

        pygame.draw.rect(dis, d_green, button_1, 1)
        pygame.draw.rect(dis, d_green, button_2, 1)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        draw_text('Play', font_style, white, dis, 275, 165)
        draw_text('Settings', font_style, white, dis, 255, 230)

        # refreshing frames
        pygame.display.flip()

        pygame.display.update()

        # 60 fps
        clock.tick(60)


main_menu()
