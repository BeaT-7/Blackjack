import os
import pygame
import time
import win32api
from Cards import *
from Scaling import *
import shutil
from PIL import Image

#scale ratio calculation
infoObject = pygame.display.Info()
scr_width, scr_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
fullW, fullH = infoObject.current_w, infoObject.current_h
ratioW = scr_width / infoObject.current_w
ratioH = scr_height / infoObject.current_h
ratio = (scr_height + scr_width) / (infoObject.current_w + infoObject.current_h)

#fonts
cfont = pygame.font.SysFont('monospace', int(26 * ratio))
bfont = pygame.font.SysFont('monospace', int(12 * ratio))
wfont = pygame.font.SysFont('monospace', int(40 * ratio))
betFont = pygame.font.SysFont('monospace', int(30 * ratio))

def playerAceCheck():
    if you.Score() > 21:
        for card in you.hand:
            if card.Value == 'Ace' and card.Points == 11:
                card.Points = 1
                continue

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
        screen.blit(pygame.image.load(f'{tempdir}\Deck_cover.png'), botHand[nr])

def Winnerr():
    global GameOn, winning
    playerAceCheck()
    if you.Score() == 21:
        if bot.Score() == 21:
            Winner = cfont.render(str(f'Draw'), 1, (255, 255, 255))
            screen.blit(Winner, WinLoc)
            you.money += winning
            bot.money += winning
            winning = 0
        elif bot.Score() <= 15:
            while bot.Score() <= 15:
                bot.GetCard(deck)
                BotAceCheck()
        elif bot.Score() != 21:
            Winner = cfont.render(str(f'{you.name} Wins'), 1, (255, 255, 255))
            screen.blit(Winner, WinLoc)
            you.money += winning * 2
            winning = 0
        EndRound()
    elif you.Score() > 21:
        Winner = cfont.render(str(f'{bot.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
        bot.money += winning * 2
        winning = 0
        EndRound()

def BWinner():
    global GameOn, winning
    if you.Score() == bot.Score():
        Winner = cfont.render(str(f'Draw'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
        you.money += winning
        bot.money += winning
        winning = 0
    elif you.Score() > bot.Score() or bot.Score() > 21:
        Winner = cfont.render(str(f'{you.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
        you.money += winning * 2
        winning = 0
    elif you.Score() < bot.Score() and bot.Score() <=21:
        Winner = cfont.render(str(f'{bot.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
        bot.money += winning * 2
        winning = 0
    EndRound()

def Visual():
    global betTimeOver
    screen.blit(pygame.image.load(f'{tempdir}\\background.png'), (0,0))
    #not enough money
    if time.time() - timeout < 3:
        msg =  wfont.render(str('You don\'t have enough money'), 1, (255, 255, 255))
        screen.blit(msg, (scr_width * 0.4, scr_height * 0.46))
    # RR button display
    if not GameOn and betTimeOver == True:
        if (time.time() - startT > 2.5):
            pygame.draw.rect(screen, (0,191,255), rrBtn)
            rrBtnText = cfont.render(str('Next Round'), 1, (255, 255, 255))
            screen.blit(rrBtnText, (rrBtn[0], rrBtn[1]+int(32*ratio)))
    # deck display
    for card in deck.Cards:
        screen.blit(card.cardPic, deckPos)
    screen.blit(pygame.image.load(f'{tempdir}\Deck_cover.png'), deckPos)
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
    #chip display
    for spot, value in enumerate(['10', '25', '50', '100', '500']):
        screen.blit(pygame.image.load(f'{tempdir}\chip{value}.png'), chipPos[spot])
    playerBet = betFont.render(str(f'Your bet: {you.bet}'), 1, (255, 255, 255))
    screen.blit(playerBet, (scr_width * 0.82, scr_height * 0.715 ))

    # winner display
    Winnerr()
    if end == True:
        BWinner()

    # point display
    YourScore = cfont.render(str(f'Your Score: {you.Score()}'), 1, (255, 255, 255))
    screen.blit(YourScore, (scr_width * 0.04, scr_height / 2 * 1.03))
    YourMoney = cfont.render(str(f'Your Money: {you.money}'), 1, (255,255,255))
    BotMoney = cfont.render(str(f'Bot Money: {bot.money}'), 1, (255,255,255))
    screen.blit(YourMoney, (scr_width * 0.04, scr_height / 2 * 1.08))
    screen.blit(BotMoney, (scr_width * 0.84, scr_height / 8 ))
    BotScore = cfont.render(str(f'Bot Score: {bot.Score()}'), 1, (255, 255, 255))
    if not GameOn:
        screen.blit(BotScore, (scr_width * 0.84, scr_height / 6.65 ))
    #buttons
    pygame.draw.ellipse(screen, (255, 70, 120), standBtn)
    standButton = cfont.render(str('STAND'), 1, (255, 255, 255))
    screen.blit(standButton, (standBtn[0]+int(9*ratio), standBtn[1]+int(32*ratio)))
    pygame.draw.ellipse(screen, (255, 70, 120), doubleBtn)
    doubleButton = cfont.render(str('DOUBLE'), 1, (255, 255, 255))
    screen.blit(doubleButton, (doubleBtn[0], doubleBtn[1]+int(32*ratio)))
    clear = pygame.image.load(f'{tempdir}/Clear.png')
    bet = pygame.image.load(f'{tempdir}/Bet.png')
    screen.blit(bet,(scr_width * 0.78, scr_height * 0.695 ))
    screen.blit(clear, (scr_width * 0.73, scr_height * 0.715 ))

    if GameOn:
        CardBlock()

    pygame.display.update()

#screen setup
screen = pygame.display.set_mode((scr_width, scr_height), pygame.FULLSCREEN)
pygame.display.set_caption('Blackjack')
background = Image.open('./Pics/TableAndHands.png')
background = background.resize((scr_width, scr_height), Image.ANTIALIAS)
background.save(f'{tempdir}\\background.png')

#buttons
standBtn = pygame.Rect(scr_width * 0.04, scr_height * 0.8, scr_width * 0.05, scr_width * 0.05)
doubleBtn = pygame.Rect(scr_width * 0.12, scr_height * 0.8, scr_width * 0.05, scr_width * 0.05)
rrBtn = pygame.Rect(scr_width * 0.46, scr_height * 0.46, scr_width * 0.08, scr_height * 0.08)

#game init
cardScale()
chipScale()
pygame.init()
clock = pygame.time.Clock()
mDown = False
coolDown = time.time()
mainLoop = True
fps = 60
aceLocation = []
WinLoc = (rrBtn[0], scr_height * 0.41)

#deck
deck = Deck()
deckPos = (scr_width/4*3.4, int(scr_height/2*ratio))
chipPos = [
    (scr_width / 4 * 3.2, scr_height / 4 * 3.1),
    (scr_width / 4 * 3.5, scr_height / 4 * 3.1),
    (scr_width / 4 * 3.05, scr_height / 4 * 3.45),
    (scr_width / 4 * 3.35, scr_height / 4 * 3.45),
    (scr_width / 4 * 3.65, scr_height / 4 * 3.45)
]
handPos = [
    (scr_width / 4 * 0.9, scr_height / 4 * 2.7),
    (scr_width / 4 * 1.3, scr_height / 4 * 2.7),
    (scr_width / 4 * 1.7, scr_height / 4 * 2.7),
    (scr_width / 4 * 2.1, scr_height / 4 * 2.7),
    (scr_width / 4 * 2.5, scr_height / 4 * 2.7)
]
botHand = [
    (scr_width / 4 * 1.3, scr_height / 4 * 0.3),
    (scr_width / 4 * 1.7, scr_height / 4 * 0.3),
    (scr_width / 4 * 2.1, scr_height / 4 * 0.3),
    (scr_width / 4 * 2.5, scr_height / 4 * 0.3),
    (scr_width / 4 * 1.3, scr_height / 4 * 0.5),
    (scr_width / 4 * 1.7, scr_height / 4 * 0.5),
    (scr_width / 4 * 2.1, scr_height / 4 * 0.5),
    (scr_width / 4 * 2.5, scr_height / 4 * 0.5)
]
#player init
you = Player('BeaT')
bot = Player('Jack')

GameOn = False
end = False
betTimeOver = False
getCards = False
double = False
timeout = time.time() - 5
while mainLoop:
    if getCards:
        you.Start(deck)
        bot.Start(deck)
        getCards = False
        time.sleep(0.01)

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
                if standBtn.collidepoint(pos) or double == True:
                    while bot.Score() <= 16:
                        bot.GetCard(deck)
                        BotAceCheck()
                    double = False
                    end = True
                if doubleBtn.collidepoint(pos):
                    you.GetCard(deck)
                    you.money -= you.bet
                    bot.money -= you.bet
                    you.bet = you.bet*2
                    winning = winning * 2
                    double = True

    aceSpots = you.Ace()
    for pos in aceSpots:
        if pos not in aceLocation:
            aceLocation.append((handPos[pos][0], handPos[pos][1], pos))

    #games mouse control on table
    if GameOn or not betTimeOver:
        if pygame.mouse.get_pressed() == (1, 0, 0):
            mPos = pygame.mouse.get_pos()
            #change Ace points
            for ace in aceLocation:
                if betTimeOver and mPos[0] >= ace[0] and mPos[1] >= ace[1] and mPos[0] <= ace[0] + int(185*ratio) and mPos[1] <= ace[1] + int(283*ratio) and mDown == False:
                    if you.hand[ace[2]].Points == 11:
                        you.hand[ace[2]].Points = 1
                    elif you.Score() + 10 <= 21:
                        you.hand[ace[2]].Points = 11
                    mDown = True
                    continue
            #get new card
            if betTimeOver and deckPos[0] <= mPos[0] <= (deckPos[0] + int(185*ratio)) and deckPos[1] <= mPos[1] <= (deckPos[1] + int(283*ratio)) and mDown == False and len(you.hand)<5 and you.Score() <= 21:
                you.GetCard(deck)
                playerAceCheck()
                mDown = True
            #add chips to bet
            if not betTimeOver and scr_width * 0.73 <= mPos[0] <= scr_width * 0.73 + int(100*ratio) and scr_height * 0.715  <= mPos[1] <= scr_height * 0.715 + int(40*ratio) and mDown == False:
                you.bet = 0
            if scr_width * 0.78 <= mPos[0] <= scr_width * 0.78 + int(80*ratio) and scr_height * 0.695 <= mPos[1] <= scr_height * 0.695 + int(80*ratio) and mDown == False and GameOn == False:
                if time.time() - coolDown >= 0.3:
                    if you.bet <= you.money:
                        coolDown = 0
                        betTimeOver = True
                        GameOn = True
                        getCards = True
                        you.money -= you.bet
                        bot.money -= you.bet
                        winning = you.bet
                        coolDown = time.time()
                        continue
                    else:
                        timeout = time.time()

            for spot, chip in enumerate(chipPos):
                if chip[0] <= mPos[0] <= chip[0]+int(100*ratio) and chip[1] <= mPos[1] <= chip[1]+int(100*ratio) and mDown == False and betTimeOver == False:
                    if spot == 0:
                        if time.time() - coolDown >= 0.3:
                            coolDown = 0
                            you.bet += 10
                            coolDown = time.time()
                            continue
                    elif spot == 1:
                        if time.time() - coolDown >= 0.3:
                            coolDown = 0
                            you.bet += 25
                            coolDown = time.time()
                            continue
                    elif spot == 2:
                        if time.time() - coolDown >= 0.3:
                            coolDown = 0
                            you.bet += 50
                            coolDown = time.time()
                            continue
                    elif spot == 3:
                        if time.time() - coolDown >= 0.3:
                            coolDown = 0
                            you.bet += 100
                            coolDown = time.time()
                            continue
                    elif spot == 4:
                        if time.time() - coolDown >= 0.3:
                            coolDown = 0
                            you.bet += 500
                            coolDown = time.time()
                            continue

        else:
            mDown = False

    #games RR
    if not GameOn and betTimeOver == True:
        if time.time() - startT > 2.5:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if rrBtn.collidepoint(pos):
                    end = False
                    you.hand = []
                    bot.hand = []
                    betTimeOver = False

#closes game
pygame.quit()

#deletes temp directory
while os.path.isdir(tempdir) == True:
    shutil.rmtree(tempdir)