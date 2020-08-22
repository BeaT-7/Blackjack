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