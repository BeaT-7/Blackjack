import pygame
import random
from Scaling import *

pygame.init()
infoObject = pygame.display.Info()

class Deck:
    def __init__(self):
        self.Cards = []
        self.Build()

    def Build(self):
        for deckNr in range(2):
            for suit in ['Spades', 'Clubs', 'Diamonds', 'Hearts']:
                for val in range(2,15):
                    self.Cards.append(Cards(suit, val))

    def Show(self):
        for card in self.Cards:
            card.Show()

    def __len__(self):
        return len(self.Cards)

class Cards:

    def __init__(self, Suit, Value):
        self.Suit = Suit
        self.Value, self.Points = self.valCheck(Value)
        self.cardPic = pygame.image.load(f'{tempdir}\{str(self.Value)}{self.Suit[:1]}.png')

    def valCheck(self, val):
        if val == 14:
            return 'Ace', 11
        elif val == 13:
            return  'King', 10
        elif val == 12:
            return  'Queen', 10
        elif val == 11:
            return 'Jack', 10
        else:
            return val, val

    def Show(self):
        print(f'{self.Value} of {self.Suit}')

class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.hand = []
        self.money = 2500

    def Start(self, deck):
        self.hand = []
        for i in range(2):
            id = random.randint(0, len(deck)-1)
            self.hand.append(deck.Cards[id])
            deck.Cards.pop(id)

    def GetCard(self, deck):
        id = random.randint(0, len(deck)-1)
        self.hand.append(deck.Cards[id])
        deck.Cards.pop(id)

    def Score(self):
        score = 0
        for card in self.hand:
            score += int(card.Points)
        return score

    def Ace(self):
        loc = []
        for spot, card in enumerate(self.hand):
            if card.Value == 'Ace' and spot not in loc:
                loc.append(spot)
        return loc

    def __len__(self):
        return len(self.hand)

