import pygame
from pygame.locals import *
import random
from utils import draw_text

pygame.init()

WIDTH, HEIGHT = 800, 800
TITLE_FONT = pygame.font.Font('mm_font.ttf',100)
COLORS = ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'pink']

class Guess():
    
    def __init__(self, guess):
        self.guess = guess

    def compare(self, game):
        right_place = 0
        right_color = 0
        game.guesses += 1
        for i in self.guess:
            if i == game.solution[self.guess.index(i)]:
                right_place += 1
            elif i in game.solution:
                right_color += 1
        return right_place, right_color

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Mastermind') # Window name
window.fill((0, 9, 30))

class RGB(Color):
    def hex_format(self):
        return '#{:02X}{:02X}{:02X}'.format(self.red,self.green,self.blue)


class Game():
    def __init__(self):
        # Create all the 10 line
        self.line = [[RGB('red')]*4]*10

        self.answerClue = [[RGB('blue')]*4]*10

        # Create the line wich the player will modify
        self.linePlayer = [RGB('grey')]*4

        # Element in linePlayer that the player will modify
        self.elementPlayerPosition = 0

        # Line number that has been validate
        self.linePlayerPosition = 0

        self.answer = self.create_answer()

        self.finish = False

    def create_answer(self):
        # Pick 4 random number between 0 and 3 (compris)

        answer = []

        for i in range(0,4):
            answer.append(RGB(COLORS[i]))

        return answer

    def changeLinePlayer(self, color):
        if self.elementPlayerPosition < 4:
            self.linePlayer[self.elementPlayerPosition] = RGB(color)
            self.createColor()
            self.elementPlayerPosition += 1

    def createColor(self):
        for idx, y in enumerate(range(1,5)):
            x = (300*y/5)+50
            y = 705
            pygame.draw.circle(window, self.linePlayer[idx], (x,y), 20)

    def createLine(self):
        if self.linePlayerPosition <= 9:
            for i, val in enumerate(self.line):
                length = 300
                rect = pygame.Surface((length,40))
                rectAnswer = pygame.Surface((length,40))
                
                # Answer rectangle
                pygame.draw.rect(rect, RGB('grey'), rect.get_rect(), border_radius = 25)

                # Clue rectangle
                pygame.draw.rect(rectAnswer, RGB('white'), rectAnswer.get_rect())

                for y, valArray in enumerate(val):
                    # Answer Space
                    circle = pygame.Surface((30,30))
                    circle.fill(RGB('grey'))
                    pygame.draw.circle(circle, valArray, (circle.get_width()/2,circle.get_height()/2), 15)
                    rect.blit(circle, (60+(50*y),5))

                    # Clue Space
                    circle = pygame.Surface((30,30))
                    circle.fill(RGB('white'))
                    pygame.draw.circle(circle, self.answerClue[len(self.answerClue) - (i+1)][y], (circle.get_width()/2,circle.get_height()/2), 15)
                    rectAnswer.blit(circle, (60+(50*y),5))
                
                window.blit(rect, (50, (50*i)+130))
                window.blit(rectAnswer, (length + 70, (50*i)+130))
            
            playing_rect = pygame.Surface((length,47))
            playing_rect.fill(RGB('white'))
            window.blit(playing_rect, (50, (50*11)+130))

    def validate(self):
        if self.linePlayer != [RGB('grey')]*4:
            self.line[(len(self.line)-1) - self.linePlayerPosition] = self.linePlayer
            self.linePlayerPosition += 1
            self.elementPlayerPosition = 0
            self.checkLineValidation()
            self.linePlayer = [RGB('grey')]*4

    
    def checkLineValidation(self):    
        clue = []
        for idx, el in enumerate(self.linePlayer):
            if self.answer[idx] == el:
                clue.append(RGB('red'))
            elif el in self.answer:
                clue.append(RGB('black'))
            else:
                clue.append(RGB('white'))

        self.answerClue[self.linePlayerPosition - 1] = clue

        if clue == [RGB('red')]*4:
            self.win()

    def win(self):
        smallfont = pygame.font.SysFont('Corbel',35)
        text = smallfont.render('Bravo Marcel tu as gagné' , True , RGB('white'))
        text2 = smallfont.render('Ton score est ' +  str(10 - self.linePlayerPosition), True , RGB('white'))
        window.blit(text, (175, 740))
        window.blit(text2, (175, 800))
        self.finish = True

def main():
    gameExit = False
    game = Game()
        
    # Create button validation
    smallfont = pygame.font.SysFont('Corbel',35)
    text = smallfont.render('Validé' , True , RGB('white'))
    window.blit(text, (175, 740))

    while not gameExit:
        for event in pygame.event.get(): 
            if event.type == QUIT:
                gameExit = True
        draw_text('MASTERMIND', TITLE_FONT, (255, 255, 255), window, (WIDTH/4)+50, 20)

        if game.finish == False:
            game.createLine()   
            game.createColor()

            choices_pos = []
            for i in range(len(COLORS)):
                x = (50*i)+400
                y = 700
                pygame.draw.circle(window, RGB(COLORS[i]), (x,y),20)
                choices_pos.append((x,y))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for position in choices_pos:
                    matching_round_x = (position[0] - 20 <= mouse_pos[0] <= position[0] + 20)
                    matching_round_y = (position[1] - 20 <= mouse_pos[1] <= position[1] + 20)
                    if matching_round_x & matching_round_y:
                        index = choices_pos.index(position)
                        game.changeLinePlayer(COLORS[index])
                    matching_text_x = (175 <= mouse_pos[0] <= 225)
                    matching_text_y = (740 <= mouse_pos[1] <= 770)
                    if matching_text_x & matching_text_y:
                        game.validate()
                        
            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(10)
        else:

main()