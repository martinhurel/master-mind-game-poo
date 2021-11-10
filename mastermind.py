import pygame
from pygame.locals import *
import random
from utils import draw_text
import time

COLORS = ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'pink']

class RGB(Color):
    def hex_format(self):
        return '#{:02X}{:02X}{:02X}'.format(self.red,self.green,self.blue)
class Game:
    def __init__(self):
        # Create all the 10 line
        self.line = [[RGB('grey')]*4]*10

        self.answerClue = [[(17,65,0)]*4]*10

        # Create the line wich the player will modify
        self.linePlayer = [RGB('grey')]*4

        # Element in linePlayer that the player will modify
        self.elementPlayerPosition = 0

        # Line number that has been validate
        self.linePlayerPosition = 0

        self.answer = self.create_answer()

        self.finish = False

        self.winning = False

        self.screen = ''

        self.choices_pos = []

        self.name = ''

    def update(self):
        # Create button validation
        pygame.init()
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',45)
        self.screen.fill((0, 9, 30))
        image = pygame.image.load("bg-wood.png")
        self.screen.blit(image, (0,0))
        self.createLine()
        self.createColor()
        self.text_validate = (55, 730)
        draw_text('MASTERMIND', game_font, (255, 255, 255), self.screen, (800/4)+50, 20)
        text_validate = smallfont.render('Validé' , True , RGB('white'))
        self.screen.blit(text_validate, self.text_validate)
        
        self.choices_pos = []
        for i in range(len(COLORS)):
            x = (40*i)+530
            y = 740
            pygame.draw.circle(self.screen, RGB(COLORS[i]), (x,y),15)
            self.choices_pos.append((x,y))
        pygame.display.update()

    def handleGameEvent(self, mouse_pos, event):
        for position in self.choices_pos:
            matching_round_x = (position[0] - 20 <= mouse_pos[0] <= position[0] + 20)
            matching_round_y = (position[1] - 20 <= mouse_pos[1] <= position[1] + 20)
            if matching_round_x & matching_round_y:
                index = self.choices_pos.index(position)
                self.changeLinePlayer(COLORS[index])
            matching_text_x = (self.text_validate[0] <= mouse_pos[0] <= self.text_validate[0] + 50)
            matching_text_y = (self.text_validate[1] <= mouse_pos[1] <= self.text_validate[1] + 50)
            if matching_text_x & matching_text_y:
                self.validate()

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
            x = 212 + (77*(y-1))
            y = 740
            pygame.draw.circle(self.screen, self.linePlayer[idx], (x,y), 13)

    def createLine(self):
        if self.linePlayerPosition <= 9:
            for i, val in enumerate(self.line):
                length = 300
                #rect = pygame.Surface((length,40))
                rectAnswer = pygame.Surface((length,40))
                
                # Clue rectangle
                pygame.draw.rect(rectAnswer, RGB('white'), rectAnswer.get_rect())

                for y, valArray in enumerate(val):
                    # Answer Space
                    self.createCircle(self.screen, valArray, 'white', 35, 35, 203+(75*y),(165+(53*i)))
                    # Clue Space
                    self.createCircle(self.screen, self.answerClue[len(self.answerClue) - (i+1)][y], 'white', 14, 14, 520+(20*y),(175+(53*i)))

    def createCircle(self, container, color, fillColor, width, height, x, y):
        circle = pygame.Surface((width,height))
        circle.fill(RGB(fillColor))
        pygame.draw.circle(circle, color, (circle.get_width()/2,circle.get_height()/2), 15)
        container.blit(circle, (x,y))


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
            self.endGame(True)

    def endGame(self, winning):
        self.winning = True
        time.sleep(0.5)
        self.finish = True

class Finish:
    def __init__(self, winning):
        self.finish = False
        self.winning = winning
        self.screen = ''
        self.name = ''

    def update(self):
        pygame.init()
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',35)
        self.screen.fill((0, 9, 30))
        draw_text('MASTERMIND', game_font, (255, 255, 255), self.screen, (800/4)+50, 20)
        draw_text('Bravo '+ self.name + ' tu as gagné', smallfont, (255, 255, 255), self.screen, 230, 250)
        pygame.display.update()

class Menu:
    def __init__(self):
        self.finish = False
        self.screen = ''
        self.text = ''

    def update(self):
        pygame.init()
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',35)
        self.screen.fill((0, 9, 30))
        
        # Rectangle Input Name
        rect_text = pygame.Surface((450,40))
        pygame.draw.rect(rect_text, RGB('white'), rect_text.get_rect())
        self.screen.blit(rect_text, (180, 290))

        # Rectangle boutton Lets play
        rect_play = pygame.Surface((200,40))
        pygame.draw.rect(rect_play, RGB('red'), rect_play.get_rect())
        self.screen.blit(rect_play, (300, 400))

        draw_text('MASTERMIND', game_font, (255, 255, 255), self.screen, 250, 20)
        draw_text('Let\'s play', smallfont, (255, 255, 255), self.screen, 350, 407)
        draw_text('Rentrez votre nom', smallfont, (255, 255, 255), self.screen, 300, 250)
        draw_text(self.text, smallfont, (RGB('black')), self.screen, 190, 300)


        pygame.display.update()      

    def handleGameEvent(self, mouse_pos, event):
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',35)
        matching_round_x = (350 - 50 <= mouse_pos[0] <= 350 + 50)
        matching_round_y = (407 - 40 <= mouse_pos[1] <= 407 + 40)
        input_active = True
        if matching_round_x & matching_round_y:
            self.finish = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text =  self.text[:-1]
            else:
                self.text += event.unicode
        self.screen.fill(0)
        
        pygame.display.flip()

class Screen:
    def __init__(self, game):
        self.running = True
        self.clock = pygame.time.Clock()
        game.screen = pygame.display.set_mode((800,800))
        self.game = game

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.game.handleGameEvent(pygame.mouse.get_pos(), event)
    
    def run(self):
        while self.game.finish == False:
            self.handling_events()
            self.game.update()
            self.clock.tick(60)

menu = Menu()
screenMenu = Screen(menu)
screenMenu.run()
game = Game()
game.name = menu.text
screen = Screen(game)
screen.run()
finish = Finish(True)
finish.name = menu.text
endGame = Screen(finish)
endGame.run()
