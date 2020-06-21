import pygame
import random

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
        self.cardPic = pygame.image.load(f'Pics\{str(self.Value)}{self.Suit[:1]}.png')

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

    def Start(self, deck):
        self.hand = []
        for i in range(2):
            id = random.randint(0, len(deck))
            self.hand.append(deck.Cards[id])
            deck.Cards.pop(id)

#52 kartis 1 decka