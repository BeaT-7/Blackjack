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
    global GameOn
    playerAceCheck()
    if you.Score() == 21:
        if bot.Score() == 21:
            Winner = cfont.render(str(f'Draw'), 1, (255, 255, 255))
            screen.blit(Winner, WinLoc)
        elif bot.Score() <= 15:
            while bot.Score() <= 15:
                bot.GetCard(deck)
                BotAceCheck()
        elif bot.Score() != 21:
            Winner = cfont.render(str(f'{you.name} Wins'), 1, (255, 255, 255))
            screen.blit(Winner, WinLoc)
        EndRound()
    elif you.Score() > 21:
        Winner = cfont.render(str(f'{bot.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
        EndRound()

def BWinner():
    global GameOn
    if you.Score() == bot.Score():
        Winner = cfont.render(str(f'Draw'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
    elif you.Score() > bot.Score() or bot.Score() > 21:
        Winner = cfont.render(str(f'{you.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
    elif you.Score() < bot.Score() and bot.Score() <=21:
        Winner = cfont.render(str(f'{bot.name} Wins'), 1, (255, 255, 255))
        screen.blit(Winner, WinLoc)
    EndRound()

def Visual():
    screen.blit(pygame.image.load(f'{tempdir}\\background.png'), (0,0))
    # RR button display
    if not GameOn:
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
pygame.init()
clock = pygame.time.Clock()
mDown = False
mainLoop = True
fps = 60
aceLocation = []
WinLoc = (rrBtn[0], scr_height * 0.41)

#deck
deck = Deck()
deckPos = (scr_width/4*3.4, int(scr_height/2*ratio))
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
                if mPos[0] >= ace[0] and mPos[1] >= ace[1] and mPos[0] <= ace[0] + 185 and mPos[1] <= ace[
                    1] + 283 and mDown == False:
                    if you.hand[ace[2]].Points == 11:
                        you.hand[ace[2]].Points = 1
                    elif you.Score() + 10 <= 21:
                        you.hand[ace[2]].Points = 11
                    mDown = True
                    continue
            #get new card
            if deckPos[0] <= mPos[0] <= (deckPos[0] + 185) and mPos[1] >= deckPos[1] and mPos[1] <= (deckPos[1] + 283) and mDown == False and len(you.hand)<5 and you.Score() <= 21:
                you.GetCard(deck)
                playerAceCheck()
                mDown = True
        else:
            mDown = False

    #games RR
    if not GameOn:
        if time.time() - startT > 2.5:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if rrBtn.collidepoint(pos):
                    you.Start(deck)
                    bot.Start(deck)
                    end = False
                    GameOn = True


#deletes temp directory
for i in range(3):
    try:
        shutil.rmtree(tempdir)
    except OSError as exc: #no such file or directory error
        if exc.errno != errno.ENOENT:
            raise
#closes game
pygame.quit()