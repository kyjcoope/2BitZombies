import pygame, time
from pygame.locals import *

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Basic Pygame program')
    coinList = []
    
    # Blit everything to the screen
    def makeList():
        coinList.append(pygame.transform.scale(pygame.image.load('coin1.png'),(20,20)))
        coinList.append(pygame.image.load('coin2.png'))
    makeList()
    screen.fill((255,255,255))
    screen.blit(coinList[0], (50, 50))
    pygame.display.update()
    lastTime = time.time()
    flipflop = True
    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.fill((255,255,255))
        if(lastTime+.5<time.time()):
            if(flipflop):          
                flipflop = False
            else:
                flipflop = True
            lastTime = time.time()
        if(flipflop):
            screen.blit(coinList[0], (50, 50))
        else:
            screen.blit(coinList[1], (50, 50))
        pygame.display.update()


if __name__ == '__main__': main()
