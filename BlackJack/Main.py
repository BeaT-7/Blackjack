import pygame
import time
from Cards import *

cfont = pygame.font.SysFont('monospace', 26)
bfont = pygame.font.SysFont('monospace', 12)
wfont = pygame.font.SysFont('monospace', 40)

def EndRound():
    global GameOn, startT
    if GameOn:
        GameOn = False
        startT = time.time()

def BotAceCheck():
    if bot.Score() > 21:
        aceloc = bot.Ace()
        for ace in aceloc:
            if bot.hand[ace].Points == 11:
                bot.hand[ace].Points = 1

def CardBlock():
    for nr in range(1, len(bot.hand)):
        screen.blit(pygame.image.load('Pics\Deck_cover.png'), botHand[nr])

def Winnerr():
    global GameOn
    if you.Score() == 21:
        if bot.Score() == 21:
            Winner = cfont.render(str(f'Draw'), 1, (255, 255, 255))
            screen.blit(Winner, (infoObject.current_w * 0.48, infoObject.current_h * 0.49))
        elif bot.Score() <= 15:
            while bot.Score() <= 15:
                bot.GetCard(deck)
                BotAceCheck()
        elif bot.Score() != 21:
            Winner = cfont.render(str(f'{you.name} Wins'), 1, (255, 255, 255))
            screen.blit(Winner, (infoObject.current_w * 0.48, infoObject.current_h * 0.49))
        EndRound()
    elif you.Score() > 21:
        Winner = cfont.render(str(f'{bot.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, (infoObject.current_w * 0.48, infoObject.current_h * 0.49))
        EndRound()

def BWinner():
    global GameOn
    if you.Score() == bot.Score():
        Winner = cfont.render(str(f'Draw'), 1, (255, 255, 255))
        screen.blit(Winner, (infoObject.current_w * 0.48, infoObject.current_h * 0.49))
    elif you.Score() > bot.Score() or bot.Score() > 21:
        Winner = cfont.render(str(f'{you.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, (infoObject.current_w * 0.48, infoObject.current_h * 0.49))
    elif you.Score() < bot.Score() and bot.Score() <=21:
        Winner = cfont.render(str(f'{bot.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, (infoObject.current_w * 0.48, infoObject.current_h * 0.49))
    EndRound()

def Visual():
    screen.blit(pygame.image.load('Pics\TableAndHands.png'), (0, 0))
    # deck display
    for card in deck.Cards:
        screen.blit(card.cardPic, deckPos)
    screen.blit(pygame.image.load('Pics\Deck_cover.png'), deckPos)
    # card display
    for spot, card in enumerate(you.hand):
        try:
            screen.blit(card.cardPic, handPos[spot])
        except IndexError:
            continue
    for spot, card in enumerate(bot.hand):
        try:
            screen.blit(card.cardPic, botHand[spot])
        except IndexError:
            continue
    # winner display
    Winnerr()
    if end == True:
        BWinner()

    # point display
    YourScore = cfont.render(str(f'Your Score: {you.Score()}'), 1, (255, 255, 255))
    screen.blit(YourScore, (infoObject.current_w * 0.04, infoObject.current_h / 2 * 1.03))
    BotScore = cfont.render(str(f'Bot Score: {bot.Score()}'), 1, (255, 255, 255))
    screen.blit(BotScore, (infoObject.current_w * 0.04, infoObject.current_h / 2 * 0.97))

    #buttons
    pygame.draw.ellipse(screen, (255, 70, 120), standBtn)
    standButton = cfont.render(str('STAND'), 1, (255, 255, 255))
    screen.blit(standButton, (standBtn[0]+9, standBtn[1]+32))
    pygame.draw.ellipse(screen, (255, 70, 120), doubleBtn)
    doubleButton = cfont.render(str('DOUBLE'), 1, (255, 255, 255))
    screen.blit(doubleButton, (doubleBtn[0], doubleBtn[1]+32))

    if GameOn == True:
        CardBlock()

    pygame.display.update()

#game init
pygame.init()
clock = pygame.time.Clock()
mDown = False
mainLoop = True
fps = 60
aceLocation = []

#screen setup
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Blackjack')

#buttons
standBtn = pygame.Rect(infoObject.current_w * 0.04, infoObject.current_h * 0.8, infoObject.current_w * 0.05, infoObject.current_w * 0.05)
doubleBtn = pygame.Rect(infoObject.current_w * 0.12, infoObject.current_h * 0.8, infoObject.current_w * 0.05, infoObject.current_w * 0.05)
rrBtn = pygame.Rect(infoObject.current_w * 0.44, infoObject.current_h * 0.44, infoObject.current_w * 0.12, infoObject.current_h * 0.12)

#deck
deck = Deck()
deckPos = (infoObject.current_w/4*3.4, infoObject.current_h/2 - 160)
handPos = [
    (infoObject.current_w / 4 * 0.9, infoObject.current_h / 4 * 2.7),
    (infoObject.current_w / 4 * 1.3, infoObject.current_h / 4 * 2.7),
    (infoObject.current_w / 4 * 1.7, infoObject.current_h / 4 * 2.7),
    (infoObject.current_w / 4 * 2.1, infoObject.current_h / 4 * 2.7),
    (infoObject.current_w / 4 * 2.5, infoObject.current_h / 4 * 2.7)
]
botHand = [
    (infoObject.current_w / 4 * 1.3, infoObject.current_h / 4 * 0.3),
    (infoObject.current_w / 4 * 1.7, infoObject.current_h / 4 * 0.3),
    (infoObject.current_w / 4 * 2.1, infoObject.current_h / 4 * 0.3),
    (infoObject.current_w / 4 * 2.5, infoObject.current_h / 4 * 0.3),
    (infoObject.current_w / 4 * 1.3, infoObject.current_h / 4 * 0.5),
    (infoObject.current_w / 4 * 1.7, infoObject.current_h / 4 * 0.5),
    (infoObject.current_w / 4 * 2.1, infoObject.current_h / 4 * 0.5),
    (infoObject.current_w / 4 * 2.5, infoObject.current_h / 4 * 0.5)
]
#player init
you = Player('BeaT')
bot = Player('Jack')
you.Start(deck)
bot.Start(deck)

GameOn = True
end = False
while mainLoop:
    clock.tick(fps)
    keys = pygame.key.get_pressed()
    pygame.mouse.get_pressed()

    #visual update
    Visual()

    #quit game
    if keys[pygame.K_ESCAPE]:
        mainLoop = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

        #buttons
        if GameOn:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if standBtn.collidepoint(pos):
                    while bot.Score() <= 16:
                        bot.GetCard(deck)
                        BotAceCheck()
                    end = True

                if doubleBtn.collidepoint(pos):
                    #double
                    pass



    aceSpots = you.Ace()
    for pos in aceSpots:
        if pos not in aceLocation:
            aceLocation.append((handPos[pos][0], handPos[pos][1], pos))

    #games mouse control on table
    if GameOn:
        if pygame.mouse.get_pressed() == (1, 0, 0):
            mPos = pygame.mouse.get_pos()
            #change Ace points
            for ace in aceLocation:
                if mPos[0] >= ace[0] and mPos[1] >= ace[1] and mPos[0] <= ace[0]+185 and mPos[1] <= ace[1]+283 and mDown == False:
                    if you.hand[ace[2]].Points == 11:
                        you.hand[ace[2]].Points = 1
                    else:
                        you.hand[ace[2]].Points = 11
                    mDown = True
                    continue
            #get new card
            if mPos[0] >= deckPos[0] and mPos[1] >= deckPos[1] and mPos[0] <= (deckPos[0]+185) and mPos[1] <= (deckPos[1]+283) and mDown == False and len(you.hand)<5 and you.Score() <= 21:
                you.GetCard(deck)
                mDown = True
        else:
            mDown = False

    #games RR
    if not GameOn:
        if (time.time() - startT > 2.5):
            pygame.draw.rect(screen, (179, 179, 0), rrBtn)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if rrBtn.collidepoint(pos):
                    you.Start(deck)
                    bot.Start(deck)
                    end = False
                    GameOn = True
pygame.quit()