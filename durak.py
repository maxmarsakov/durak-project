#!/usr/bin/pythonw
# -*- coding: utf-8 -*-

from baseGame import BaseGame
from deck import DeckType
from player import Player
from move import Move
from os import system, name
from console import print_
from translation import getText, checkLanguageAvailable, setLanguage, getAvailableLanguages
import random

# define our clear function 
def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

#!/usr/bin/python
# -*- coding: utf-8 -*-

class Durak(BaseGame):
    def __init__(self, players, deckType, cardsInHand):
        super(Durak, self).__init__(players, deckType, cardsInHand)
        self.trumpCard = None

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

def startGame():
    # Select game language
    language_exist = False
    while (not language_exist):
        language = input(getText('SELECT_LANGUAGE').format(getAvailableLanguages()))
        if(checkLanguageAvailable(language)):
            setLanguage(language)
            language_exist = True
        else:
            print_ (getText('WRONG_LANGUAGE'))

    clear()

    name = input(getText('PLAYER_NAME'))
    # TODO for tests set 1 card
    durak = Durak([Player(name), Player('bot', True)], DeckType.Card36, 6)
    durak.fillDeck()
    durak.shuffleDeck()
    durak.defineTrump()
    durak.handOverCards()
    move = None
    loser = (None, None)
    while (not loser[0]):
        players = durak.nextPlayers(move)
        playerMove = players[0]
        playerDefense = players[1]
        move = Move(durak.trumpCard, playerMove, playerDefense)

        while(move.isOver == False and not loser[0]):
            playerMove.setCurrentMove(move)
            playerDefense.setCurrentMove(move)
            loser = durak.checkLoserExist()

        if(loser[0]):
            if(loser[1]!=getText('EXIT')): startGame()
            return
        
        durak.handOverCards()

# Enter point
startGame()