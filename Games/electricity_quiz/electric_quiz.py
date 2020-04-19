#!/usr/bin/python
#Electric Quiz Game for MC Green robot
#Designed and written by Manas Harbola (harbolam@mcvts.net) on behalf of Middlesex County Academy

import pygame
import json
from PIL import Image
import random
import sys
sys.path.append("../")
from face_controller import Face_comm
#Screen size of window
window_size = (1920,1080)

#Max FPS (frames per second) of game
FPS = 30

#Define basic colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
darker_red = (200, 0, 0)
green = (0, 255, 0)
darker_green = (0, 200, 0)
blue = (50, 89, 250)
darker_blue = (35, 67, 250)
yellow = (255, 255, 0)
darker_yellow = (200, 200, 0)

#Load questions JSON file
with open('questions.json', 'r') as file:
    data = json.load(file)

#Define background
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, window_size)
backgroundRect = background.get_rect()

#Class for generating buttons
class Button:
    def __init__ (self, surfaceName, ac, ic, rectVals, text, font):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button
        self.surfaceName = surfaceName
        self.text = text
        self.font = font

    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.surfaceName, self.ac, self.rectAttrs)

        #Else just show darker button
        else:
            pygame.draw.rect(self.surfaceName, self.ic, self.rectAttrs)

        textSurf, textRect = text_objects(self.text, self.font)

        textRect.center = (x + (w / 2), y + (h / 2))
        self.surfaceName.blit(textSurf, textRect)
        pygame.display.update(self.get_rect())

    def get_rect(self):
        x, y, w, h = self.rectAttrs
        return pygame.rect.Rect(x, y, w, h)

    def is_pressed(self, touch_status):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()
        
        #Check if mouse is hovering over button or not
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if touch_status == True:
                #print('CLICK DETECTED')
                return True

            elif touch_status == False:
                return False

        #If mouse is not hovering over button, button must obviously not be pressed
        else:
            return False

#Render text to a surface and a corresponding rectangle
def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def makeFace():
    #There are 8 total possible faces (first being happy)
    #Just randomly choose between the first three faces
    faces [1,2,3,4,5,6,7,8]
    Face_comm.face_update
    faceNum = 0
    return faceNum


#Generate Electric Bar for game WORKS
def generate_bar(surfaceName, x, y, num_right, num_wrong, num_questions, color):
    #Fixed width for full size bar
    fixed_width = 1500 / 2
    #Fixed height for full size bar
    fixed_height = 100 / 2
    
    width_div = fixed_width / num_questions
    
    #Calculate width of bar
    w = max((width_div * num_right) - (0.5 * width_div * num_wrong), 0)
    
    #Draw electricity bar
    pygame.draw.rect(surfaceName, color, (x, y, w, fixed_height))
    #Draw electricity bar outline
    pygame.draw.rect(surfaceName, blue, (x, y, fixed_width, fixed_height), 3)

def generate_q_page(surfaceName, status, pt_inc, question, choices, correct_ans):
    #Status is a list [score, num_right, num_wrong, num_questions]

    #Button dimensions
    button_w = 750 / 2; button_h = 250 / 2
    
    #Reference x, y coordinates for upper left button
    ref_x = window_size[0] / 4 + 50; ref_y = window_size[1] / 4;

    row_spacing = button_w + (0.5 * 200)
    column_spacing = button_h + (0.5 * 200)

    #Shuffle answers from choices
    random.shuffle(choices)

    buttonText = pygame.font.Font('FreeSansBold.ttf', 32)

    up_left_button = Button(surfaceName, darker_red, red, (ref_x, ref_y, button_w, button_h), choices[0], buttonText)
    up_right_button = Button(surfaceName, darker_blue, blue, (ref_x + row_spacing, ref_y, button_w, button_h), choices[1], buttonText)
    bottom_left_button = Button(surfaceName, darker_yellow, yellow, (ref_x, ref_y + column_spacing, button_w, button_h), choices[2], buttonText)
    bottom_right_button = Button(surfaceName, darker_green, green, (ref_x + row_spacing, ref_y + column_spacing, button_w, button_h), choices[3], buttonText)

    #Need to include rects here for selective updating later

    #Prepare question text and location
    QuestionSurf, QuestionRect = text_objects(question, largeText, yellow)
    QuestionRect.center = ((window_size[0] / 2), (window_size[1] / 8))

    ScoreSurf, ScoreRect = text_objects('Score: ' + str(status[0]) + ' points', mediumText, yellow)
    ScoreRect.center = ((0.80 * window_size[0]), (window_size[1] / 16))
    
    ElectricSurf, ElectricRect = text_objects('Electric Bar: ', mediumText, yellow)
    ElectricRect.topleft = ((0.10 * window_size[0]), (0.70 * window_size[1]))

    #Make entire screen 'white' to 'clean' it
    surfaceName.fill(white)

    surfaceName.blit(background, backgroundRect)

    #Write text to buffer
    surfaceName.blit(QuestionSurf, QuestionRect)
    surfaceName.blit(ScoreSurf, ScoreRect)
    surfaceName.blit(ElectricSurf, ElectricRect)

    #Generate Electric bar
    generate_bar(surfaceName, 0.25 * window_size[0], 0.80 * window_size[1], status[1], status[2], status[3], yellow)

    up_left_rect = up_left_button.get_rect()
    up_right_rect = up_right_button.get_rect()
    bottom_left_rect = bottom_left_button.get_rect()
    bottom_right_rect = bottom_right_button.get_rect()
    
    updateList = [up_left_rect, up_right_rect, bottom_left_rect, bottom_right_rect]
    
    #Update ENTIRE screen just once
    pygame.display.update()

    running = True

    answer_choice = 'not_answered'

    while running:
        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if up_left_button.is_pressed(touch_status):
                    if up_left_button.text == correct_ans:
                        answer_choice = 'correct'
                    else:
                        answer_choice = 'incorrect'

                if up_right_button.is_pressed(touch_status):
                    if up_right_button.text == correct_ans:
                        answer_choice = 'correct'
                    else:
                        answer_choice = 'incorrect'

                if bottom_left_button.is_pressed(touch_status):
                    if bottom_left_button.text == correct_ans:
                        answer_choice = 'correct'
                    else:
                        answer_choice = 'incorrect'

                if bottom_right_button.is_pressed(touch_status):
                     if bottom_right_button.text == correct_ans:
                        answer_choice = 'correct'
                     else:
                        answer_choice = 'incorrect'

                if answer_choice == 'correct':
                   return 'correct'

                elif answer_choice == 'incorrect':
                   return 'incorrect'
            else:
                touch_status = False

        up_left_button.generate()
        up_right_button.generate()
        bottom_left_button.generate()
        bottom_right_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)

def generate_correct_page(surface, status, point_inc):
    next_button = Button(surface, darker_blue, blue, (0.5 * window_size[0] - (0.5 * 375), 0.5 * window_size[1], 750 / 2, 250 / 2), 'Next Question', mediumText)

    next_button_rect = next_button.get_rect()
    updateList = [next_button_rect]

    HeadingSurf, HeadingRect = text_objects('Correct!', largeText)
    HeadingRect.center = ((window_size[0] / 2), (window_size[1] / 4))

    ScoreSurf, ScoreRect = text_objects('Score: ' + str(status[0]) + ' (+' + str(point_inc) + ' pts)', mediumText)
    ScoreRect.center = ((window_size[0] / 2), (0.35 * window_size[1]))
    
    ElectricSurf, ElectricRect = text_objects('Electric Bar: ', mediumText)
    ElectricRect.topleft = ((0.10 * window_size[0]), (0.70 * window_size[1]))


    surface.fill(green)


    surface.blit(HeadingSurf, HeadingRect)
    surface.blit(ScoreSurf, ScoreRect)
    surface.blit(ElectricSurf, ElectricRect)
    generate_bar(surface, 0.25 * window_size[0], 0.80 * window_size[1], status[1], status[2], status[3], yellow)


    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('Pressed')
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if next_button.is_pressed(touch_status):
                    running = False
            else:
                touch_status = False

        #surface.fill(white)
        next_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)

def generate_incorrect_page(surface, status, point_dec, correct_ans):
    next_button = Button(surface, darker_blue, blue, (0.5 * window_size[0] - (0.5 * 375), 0.5 * window_size[1], 750 / 2, 250 / 2), 'Next Question', mediumText)

    next_button_rect = next_button.get_rect()
    updateList = [next_button_rect]

    line_spacing = 100 / 2

    HeadingSurf, HeadingRect = text_objects('Sorry!', largeText)
    HeadingRect.center = ((window_size[0] / 2), (0.2 * window_size[1]))

    Heading2Surf, Heading2Rect = text_objects('Correct Answer Was:', mediumText)
    Heading2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + line_spacing)

    AnswerSurf, AnswerRect = text_objects(correct_ans, mediumText)
    AnswerRect.center = ((window_size[0] / 2), (0.25 * window_size[1]) + (2.5 * line_spacing))


    ScoreSurf, ScoreRect = text_objects('Score: ' + str(status[0]) + ' (-' + str(point_dec) + ' pts)', mediumText)
    ScoreRect.center = ((window_size[0] / 2), (0.25 * window_size[1]) + (4 * line_spacing))
    
    ElectricSurf, ElectricRect = text_objects('Electric Bar: ', mediumText)
    ElectricRect.topleft = ((0.10 * window_size[0]), (0.70 * window_size[1]))

    surface.fill(red)

    surface.blit(HeadingSurf, HeadingRect)
    surface.blit(Heading2Surf, Heading2Rect)
    surface.blit(AnswerSurf, AnswerRect)
    surface.blit(ScoreSurf, ScoreRect)
    surface.blit(ElectricSurf, ElectricRect)

    generate_bar(surface, 0.25 * window_size[0], 0.80 * window_size[1], status[1], status[2], status[3], yellow)


    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('Pressed')
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if next_button.is_pressed(touch_status):
                    running = False
            else:
                touch_status = False

        #surface.fill(white)
        next_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)

def makeFace():
    #IMPLEMENT ROS CONNECTION HERE
    pass


#Initiate pygame
pygame.init() #SUPER IMPORTANT

#Define basic text sizes
largeText = pygame.font.Font('FreeSansBold.ttf', 64)   #Large text, ideal for headings
mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   #Medium text, ideal for subheadings
smallText =  pygame.font.Font('FreeSansBold.ttf', 16)   #Small text, ideal for small buttons

#Instantiate window/surface
gameDisplay = pygame.display.set_mode(window_size)
pygame.display.set_caption('Electric Quiz')
clock = pygame.time.Clock()

#Start Menu for Game
def game_intro(surface):
    #Button Dimensions
    button_w = 750 / 2; button_h = 250 / 2
    help_button_x = 270; button_y = 1300 / 2
    button_spacing = 237 / 2 #spacing between buttons in px
    play_button_x = help_button_x + button_w + button_spacing
    quit_button_x = play_button_x + button_w + button_spacing
    

    #Instantiate buttons (Only needs to be done once)
    help_button = Button(surface, darker_blue, blue, (help_button_x, button_y, button_w, button_h), 'Help', mediumText)
    play_button = Button(surface, darker_green, green, (play_button_x, button_y, button_w, button_h), 'Play', mediumText)
    quit_button = Button(surface, darker_red, red, (quit_button_x, button_y, button_w, button_h), 'Quit', mediumText)
    
    #Portion of the screen that must ONLY be updated
    help_button_rect = help_button.get_rect()
    play_button_rect = play_button.get_rect()
    quit_button_rect = quit_button.get_rect()
    updateList = [help_button_rect, play_button_rect, quit_button_rect]

    #Prepare title text and location
    TextSurf, TextRect = text_objects('MC Green Electric Quiz!', largeText, yellow)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))

    #Make entire screen white to clean it
    surface.fill(white)

    surface.blit(background, backgroundRect)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)

    #Update ENTIRE screen just once
    pygame.display.update()

    touch_status = False #False = no touch, True = touch present

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('Pressed')
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if quit_button.is_pressed(touch_status):    #If 'Quit' button is tapped
                    pygame.quit()
                    quit()

                if play_button.is_pressed(touch_status):    #If 'Play' button is tapped
                    #game_menu(gameDisplay)
                    select_level(gameDisplay)
                if help_button.is_pressed(touch_status):    #If 'Help' button is tapped
                    game_help(gameDisplay)
            else:
                touch_status = False

        help_button.generate()
        play_button.generate()
        quit_button.generate()

        #Update only the portions that need to be updated
        pygame.display.update(updateList)
        clock.tick(FPS)

#Help Menu for Game
def game_help(surface):
    #Instantiate button for returning back to intro page
    back_button = Button(surface, darker_green, green, (0.5 * window_size[0] - (0.5 * 375), 0.75 * window_size[1], 750 / 2, 250 / 2), 'Back', mediumText)

    #back_button_rect = pygame.rect.Rect(back_button.rectAttrs[0], back_button.rectAttrs[1], back_button.rectAttrs[2], back_button.rectAttrs[3])
    back_button_rect = back_button.get_rect()
    updateList = [back_button_rect]
    
    TextSurf, TextRect = text_objects('How to Play:', largeText, yellow)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))
    
    line_spacing = 75   #Spacing between each line of instructions

    Line1Surf, Line1Rect = text_objects('1.) Read each question carefully and select the best answer', mediumText, yellow)
    Line1Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (0.5 * 300))
    
    Line2Surf, Line2Rect = text_objects('2.) If your answer is correct, you will earn points and charge your electricity meter', pygame.font.Font('FreeSansBold.ttf', 40), yellow)
    Line2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (300 / 2) + (2 * line_spacing))

    Line3Surf, Line3Rect = text_objects('3.) If your answer is incorrect, you will lose points and your charge meter will go down', pygame.font.Font('FreeSansBold.ttf', 40), yellow)
    Line3Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + (300 / 2) + (4 * line_spacing))


    #Make entire screen white to clean it
    surface.fill(white)
    
    surface.blit(background, backgroundRect)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)
    surface.blit(Line1Surf, Line1Rect)
    surface.blit(Line2Surf, Line2Rect)
    surface.blit(Line3Surf, Line3Rect)

    #Update ENTIRE screen just once
    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('Pressed')
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if back_button.is_pressed(touch_status):
                    #print('Intro Activated')
                    game_intro(gameDisplay)
            else:
                touch_status = False

        #surface.fill(white)
        back_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)

def select_level(surface):
    #Instantiate button for returning back to intro page
    button_w, button_h = 375, 125

    back_button = Button(surface, darker_green, green, (0.5 * window_size[0] - (0.5 * 375), 0.75 * window_size[1], button_w, button_h), 'Back', mediumText)

    x = (window_size[0] - (4 * button_w)) / 2

    easy_button = Button(surface, darker_green, green, (x, 0.50 * window_size[1], button_w, button_h), 'Easy', mediumText)
    medium_button = Button(surface, darker_yellow, yellow, (x +1.5 * button_w, 0.50 * window_size[1], button_w, button_h), 'Medium', mediumText)
    hard_button = Button(surface, darker_red, red, (x + 3 * button_w, 0.50 * window_size[1], button_w, button_h), 'Hard', mediumText)


    back_button_rect = back_button.get_rect()
    easy_button_rect = easy_button.get_rect()
    medium_button_rect = medium_button.get_rect()
    hard_button_rect = hard_button.get_rect()
    
    updateList = [back_button_rect, easy_button_rect, medium_button_rect, hard_button_rect]
    
    TextSurf, TextRect = text_objects('Select your level:', largeText, yellow)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))
    
    line_spacing = 75   #Spacing between each line of instructions

    #Make entire screen white to clean it
    surface.fill(white)

    surface.blit(background, backgroundRect)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)

    #Update ENTIRE screen just once
    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if back_button.is_pressed(touch_status):
                    game_intro(gameDisplay)
                if easy_button.is_pressed(touch_status):
                    point_vals = data["point_vals"]["level_easy"]
                    q_set = [q for q in data["level_easy"]]
                    game_menu(gameDisplay, point_vals, q_set)
                if medium_button.is_pressed(touch_status):
                    point_vals = data["point_vals"]["level_medium"]
                    q_set = [q for q in data["level_medium"]]
                    game_menu(gameDisplay, point_vals, q_set)
                if hard_button.is_pressed(touch_status):
                    point_vals = data["point_vals"]["level_hard"]
                    q_set = [q for q in data["level_hard"]]
                    game_menu(gameDisplay, point_vals, q_set)

            else:
                touch_status = False

        #surface.fill(white)
        back_button.generate()
        easy_button.generate()
        medium_button.generate()
        hard_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)



def game_menu(surface, point_vals, q_set):
    #Status is a list [score, num_right, num_wrong, num_questions]
    status = [0, 0, 0, len(q_set)]

    #Randomize order of questions
    #random.shuffle(questions)
    random.shuffle(q_set)
     
    for q in q_set:
        #do something 
        correct_ans = q["answer"]
        pt_inc = point_vals[0]
        pt_dec = point_vals[1]
        question = q["question"]
        correct_ans = q["answer"]
        choices = q["choices"]
        outcome = generate_q_page(surface, status, pt_inc, question, choices, correct_ans)
 
        if outcome == 'correct':
            status[0] += pt_inc
            status[1] += 1
            generate_correct_page(surface, status, pt_inc)

        elif outcome == 'incorrect':
            if (status[0] != 0):
                status[0] -= pt_dec

            status[2] += 1
            generate_incorrect_page(surface, status, pt_dec, correct_ans)

    game_over(surface, status)

def game_over(surface, status):
    #Button Dimensions
    button_w = 750 / 2; button_h = 250 / 2

    quit_button = Button(surface, darker_red, red, (window_size[0] / 2 - (0.5 * 375), 0.75 * window_size[1], button_w, button_h), 'Quit', mediumText)

    quit_button_rect = quit_button.get_rect()

    updateList = [quit_button_rect]


    #Prepare title text and location
    TextSurf, TextRect = text_objects('Game Over!', largeText)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))

    FinalSurf, FinalRect = text_objects('Final Score: ' + str(status[0]) + ' pts', mediumText)
    FinalRect.center = ((window_size[0] / 2), (0.4 * window_size[1]))

    ElectricSurf, ElectricRect = text_objects('Electric Bar: ', mediumText)
    ElectricRect.topleft = ((0.10 * window_size[0]), (0.55 * window_size[1]))

    #Make entire screen white to clean it
    surface.fill(green)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)
    surface.blit(FinalSurf, FinalRect)
    surface.blit(ElectricSurf, ElectricRect)
    generate_bar(surface, 0.25 * window_size[0], 0.65 * window_size[1], status[1], status[2], status[3], yellow)

    #Update ENTIRE screen just once
    pygame.display.update()

    touch_status = False

    running = True
    
    #makeFace()

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('Pressed')
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if quit_button.is_pressed(touch_status):    #If 'Quit' button is tapped
                    pygame.quit()
                    quit()

            else:
                touch_status = False

        quit_button.generate()

        #Update only the portions that need to be updated
        pygame.display.update(updateList)
        clock.tick(FPS)

#Execute game
game_intro(gameDisplay)

pygame.quit()
quit()
