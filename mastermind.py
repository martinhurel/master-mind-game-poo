import pygame
from pygame.locals import *
import random
from utils import draw_text

pygame.init()

WIDTH, HEIGHT = 800, 800
TITLE_FONT = pygame.font.Font('mm_font.ttf',100)
COLORS = ['blue', 'red', 'green', 'yellow', 'purple', 'white', 'orange']
white = (255,255,255)
light_gray = (219, 219, 219)
gray = (147, 147, 147)
dark_gray = (84, 84, 84)
red = (255, 54, 54)

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Mastermind') # Window name
window.fill((0, 9, 30))

class RGB(Color):
    def hex_format(self):
        return '#{:02X}{:02X}{:02X}'.format(self.red,self.green,self.blue)

def main():
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
        for y in range(1,5):
            pygame.draw.circle(window, light_gray, ((length*y/5)+50,705), 20)

        choices = pygame.Surface((300,300))
        choices.fill(white)


        # Choices bubble
        pos = 10
        for color in COLORS:
            circle = pygame.Surface((30,30))
            circle.fill(white)
            pygame.draw.circle(circle, RGB(color), (circle.get_width()/2,circle.get_height()/2), 15)
            choices.blit(circle, (pos, 10))
            pos += 50
        window.blit(choices, (450, 200))
        



        

        pygame.display.update()

def menu(surface):
    draw_text('MASTERMIND', TITLE_FONT, (255, 255, 255), surface, (WIDTH/4)+50, 60)
        
def game(surface):
    solution = random.sample(colors,4)


main()