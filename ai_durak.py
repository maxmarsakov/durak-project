"""
Modified Durak class for our purposes
"""
from baseGame import BaseGame
from deck import DeckType,Deck
from player import Player
from move import Move
from os import system, name
from console import print_
from translation import getText
import random

class Durak(BaseGame):
    def __init__(self, players, deckType, cardsInHand):
        """
        cardsInHand - how much cards in hand
        TODO: players are agents now
        """
        if(type(deckType) != DeckType): raise Exception(getText('CANT_DEFINE_DECK'))
        self._players = players
        self._deck = Deck(deckType)
        self._cardsInHand = cardsInHand
        self.trumpCard = None

    """
    from baseGame
    """
    def fillDeck(self):
        self._deck.fillDeck()

    def shuffleDeck(self):
        self._deck.shuffleDeck()

    def handOverCards(self):
        s = ''
        for player in self._players:
            s += player.handOverCards(self._deck, self._cardsInHand)
        print_(s.rstrip(), endWith='\n', startWith='\n')

    def defineTrump(self):
        cardNumber = random.randint(0, len(self._deck.cards) - 1)
        self.trumpCard = self._deck.cards.pop(cardNumber)
        self._deck.cards.insert(0, self.trumpCard)
        for card in self._deck.cards:
            if(card.suit == self.trumpCard.suit):
                card.value += 100
        print_(getText('TRUMP_CARD_IN_DECK').format(self.trumpCard.fullName()))

    def __defineFirstMovePlayer(self):
        if (self.trumpCard == None):
            print_ (getText('TRUMP_NOT_DEFINED'))
            return None
        minPlayerCard = {}
        for player in self._players:
            cards = filter(lambda x: x.suit == self.trumpCard.suit, player.cards)
            minCard = min(cards, key=lambda x: x.number, default=None)
            if(minCard is None): continue
            minPlayerCard[player] = minCard
        playerFirstMove = min(minPlayerCard.items(), key=lambda x: x[1].number, default=None)
        if(playerFirstMove is None):
            print_ (getText('PLAYERS_HAVE_NOT_TRUMPS'))
            index = random.randint(0, len(self._players)-1)
            playerFirstMove = self._players[index]
        else:
            playerFirstMove = playerFirstMove[0]
        return playerFirstMove

    def __nextPlayer(self):
        if(len(self._players) < 2):
            print_ (getText('NEED_TWO_PLAYERS'))
            return

        try:
            self.__currentPlayer
        except AttributeError:
            self.__currentPlayer = self.__defineFirstMovePlayer()
            return self.__currentPlayer

        if(self.__currentPlayer is None):
            print_ (getText('FIRST_PLAYER_NOT_DEFINED'))
            return    
        index = self._players.index(self.__currentPlayer) + 1
        if(index > len(self._players) - 1):
            return self._players[0]
        else:
            return self._players[index]

    def nextPlayers(self, move = None):
        if(move is not None and len(move.cards) % 2 != 0):
            self.__currentPlayer = self.__nextPlayer()
        self.__currentPlayer = self.__nextPlayer() 
        return (self.__currentPlayer, self.__nextPlayer())

    def checkLoserExist(self):
        playersWithCard = []
        for player in self._players:
            if(len(player.cards) > 0):
                playersWithCard.append(player)
        if(len(playersWithCard) == 1):
            print_ (getText('PLAYER_LOSE').format('\033[44m', '\033[91m', playersWithCard[0].name, '\033[00m'), startWith='\n', endWith='\n')
            command = input (getText('END_OR_RESTART_GAME').format('\033[95m', '\033[00m'))
            return (True, command)
        elif(len(playersWithCard) == 0):
            print_ (getText('PLAYERS_PLAY_DRAW').format('\033[44m', '\033[91m', '\033[00m'), startWith='\n', endWith='\n')
            command = input (getText('END_OR_RESTART_GAME').format('\033[95m', '\033[00m'))
            return (True, command)
        else: 
            return (False, None)
