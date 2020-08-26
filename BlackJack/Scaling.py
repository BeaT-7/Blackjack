import tempfile
import pygame
import win32api
from PIL import Image
from Cards import *
pygame.init()

infoObject = pygame.display.Info()
scr_width, scr_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
fullW, fullH = infoObject.current_w, infoObject.current_h
ratioW = scr_width / infoObject.current_w
ratioH = scr_height / infoObject.current_h
ratio = (scr_height + scr_width) / (infoObject.current_w + infoObject.current_h)

#creates temp directory
tempdir = tempfile.mkdtemp(dir='./Pics', prefix=None, suffix=None)
def cardScale():
    for suit in ['S', 'C', 'D', 'H']:
        for val in [2,3,4,5,6,7,8,9,10,'Jack','Queen', 'King', 'Ace']:
            card = Image.open(f'./Pics/{val}{suit}.png')
            card = card.resize((int(185*ratio), int(283*ratio)), Image.ANTIALIAS)
            card.save(f'{tempdir}/{val}{suit}.png')
    cover = Image.open(f'./Pics/Deck_cover.png')
    cover = cover.resize((int(185*ratio), int(283*ratio)), Image.ANTIALIAS)
    cover.save(f'{tempdir}/Deck_cover.png')

def chipScale():
    for chip in ['10', '25', '50', '100', '500']:
        chips = Image.open(f'./Pics/chip{chip}.png')
        chips = chips.resize((int(100*ratio), int(100*ratio)), Image.ANTIALIAS)
        chips.save(f'{tempdir}/chip{chip}.png')
    clearBtn = Image.open(f'./Pics/Clear.png')
    clearBtn = clearBtn.resize((int(100*ratio), int(40*ratio)), Image.ANTIALIAS)
    clearBtn.save(f'{tempdir}/Clear.png')
    betBtn = Image.open(f'./Pics/Bet.png')
    betBtn = betBtn.resize((int(80*ratio), int(80*ratio)), Image.ANTIALIAS)
    betBtn.save(f'{tempdir}/Bet.png')