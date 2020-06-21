import pygame
import time
import random
from Cards import *

def Visual():
    screen.blit(pygame.image.load('Pics\TableAndHands.png'), (0,0))
    for card in deck.Cards:
        screen.blit(card.cardPic, deckPos)
    screen.blit(pygame.image.load('Pics\Deck_cover.png'), deckPos)
    for spot, card in enumerate(you.hand):
        screen.blit(card.cardPic, handPos[spot])

    pygame.display.update()

#game init
pygame.init()
clock = pygame.time.Clock()

#screen setup
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Blackjack')

#deck
deck = Deck()
deckPos = (infoObject.current_w/4*3.4, infoObject.current_h/2 - 160)
handPos = [(infoObject.current_w/4*1.5, infoObject.current_h/4*2.7), (infoObject.current_w/4*1.9, infoObject.current_h/4*2.7)]

you = Player('BeaT')
you.Start(deck)

mainLoop = True
fps = 60
while mainLoop:
    clock.tick(fps)
    keys = pygame.key.get_pressed()

    # exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    if keys[pygame.K_ESCAPE]:
        mainLoop = False

    #ss

    #visual update
    Visual()


pygame.quit()