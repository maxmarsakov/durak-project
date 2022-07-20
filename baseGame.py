from deck import Deck, DeckType
from player import Player
from console import print_
from translation import getText
import random

class BaseGame: 
    def __init__(self, players, deckType, cardsInHand):
        if(type(deckType) != DeckType): raise Exception(getText('CANT_DEFINE_DECK'))
        self._players = players
        self._deck = Deck(deckType)
        self._cardsInHand = cardsInHand

    def fillDeck(self):
        self._deck.fillDeck()

    def shuffleDeck(self):
        self._deck.shuffleDeck()

    def handOverCards(self):
        s = ''
        for player in self._players:
            s += player.handOverCards(self._deck, self._cardsInHand)
        print_(s.rstrip(), endWith='\n', startWith='\n')