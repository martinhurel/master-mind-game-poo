import pygame
from pygame.locals import *
import random
from utils import draw_text

pygame.init()

WIDTH, HEIGHT = 800, 800
TITLE_FONT = pygame.font.Font('mm_font.ttf',100)
COLORS = ['blue', 'red', 'green', 'yellow', 'purple', 'white', 'orange', 'pink']
white = (255,255,255)
light_gray = (219, 219, 219)
gray = (147, 147, 147)
dark_gray = (84, 84, 84)
red = (255, 54, 54)
blue = (35, 0, 255)
green = (0, 213, 65)
yellow = (255, 195, 0)
slot = 0

class RGB(Color):
    def hex_format(self):
        return '#{:02X}{:02X}{:02X}'.format(self.red,self.green,self.blue)

slots_colors = [RGB("gray")]*4

class Game():

    def __init__(self, difficulty = 2):
        self.difficulty = difficulty
        self.solution = random.sample(colors,4)
        self.guesses = 0
        self.right_places = 0

    def play(self):
        while self.guesses <= 10 and self.right_places != 4:
            player_input = random.sample(colors,4) 
            guess = Guess(player_input) 
            print('Guess number',self.guesses,':',guess.guess)
            self.right_places = guess.compare(self)[0]
        print(self.solution)

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

def main(slot):
    gameExit = False
    while not gameExit:
        for event in pygame.event.get(): 
            if event.type == QUIT:
                gameExit = True
        menu(window)

        for i in range(1,11):
            length = 300
            rect = pygame.Surface((length,40))
            #rect.fill(red)
            pygame.draw.rect(rect, gray, rect.get_rect(), border_radius = 25)

            for y in range(1,5):
                circle = pygame.Surface((30,30))
                circle.fill(gray)
                pygame.draw.circle(circle, red, (circle.get_width()/2,circle.get_height()/2), 15)
                rect.blit(circle, (10+(50*y),5))
            
            window.blit(rect, (50, (50*i)+130))
        
        playing_rect = pygame.Surface((length,40))
        playing_rect.fill(gray)
        window.blit(playing_rect, (50, (50*11)+130))

        # slots_colors = [RGB("gray")]*4
        for i in range(0,4):
            x = (length*(i+1)/5)+50
            y = 705
            pygame.draw.circle(window, slots_colors[i], (x,y), 20)

        choices_pos = []
        for i in range(len(COLORS)):
            x = (50*i)+400
            y = 700
            pygame.draw.circle(window, RGB(COLORS[i]), (x,y),20)
            choices_pos.append((x,y))

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for position in choices_pos:
                matching_x = (position[0] - 20 <= mouse_pos[0] <= position[0] + 20)
                matching_y = (position[1] - 20 <= mouse_pos[1] <= position[1] + 20)
                if matching_x & matching_y:
                    index = choices_pos.index(position)
                    color = COLORS[index]
                    slots_colors[slot] = RGB(color)
                    slot += 1
            
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

def menu(surface):
    draw_text('MASTERMIND', TITLE_FONT, (255, 255, 255), surface, (WIDTH/4)+50, 60)
        
def game(surface):
    solution = random.sample(colors,4)

main(slot)