from enum import Enum
from card import Card
from console import print_
from translation import getText
import random

class DeckType(Enum):
    Card36 = 1,
    Card52 = 2

class Deck:
    __suits = ['♦','♥','♣','♠']
    __cardset = {'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'10': 10,'J': 11,'Q': 12,'K': 13,'A': 14}

    def __init__(self, deckType):
        if(type(deckType) != DeckType): raise Exception(getText('INCORRECT_DECK_TYPE'))
        self.__deckType = deckType

    def fillDeck(self):
        self.cards = []
        iterator = 1

        # # # TODO for tests
        # self.cards.append(Card('6', '♥', 1, 1))
        # self.cards.append(Card('7', '♥', 1, 2))
        # return

        for suit in self.__suits:
            for key,value in self.__cardset.items():
                if(self.__deckType == DeckType.Card36 and value < 6):
                    continue
                self.cards.append(Card(key, suit, iterator, value))
                iterator += 1
        print_ (getText('DECK_FILLED_BY_COUNT').format(str(len(self.cards))))
    
    def shuffleDeck(self):
        if(len(self.cards) == 0):
            print_ (getText('NO_CARDS_IN_DECK'))
            return
        random.shuffle(self.cards)
        print_ (getText('DECK_SHUFFLED'))
