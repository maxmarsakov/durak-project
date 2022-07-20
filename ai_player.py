"""
adaptation for ai player
"""
from card import Card
from console import print_
from translation import getText

class Player:
    def __init__(self, name, isBot = False):
        self.name = name
        self.isBot = isBot
        self.cards = []

    def handOverCards(self, deck, count):
        s = ''
        if(len(deck.cards) == 0):
            s += getText('NO_CARDS_IN_DECK') + '\n'
            return s
        destLength = count - len(self.cards)
        iterator = 0
        if(destLength <= 0):
            s += getText('PLAYER_DOESNT_NEED_CARDS').format(self.name) + '\n'
            return s
        while (iterator != destLength and len(deck.cards) != 0):
            self.cards.append(deck.cards.pop())
            iterator += 1
        s += getText('PLAYER_TAKE_COUNT_CARDS').format(self.name, str(destLength)) + '\n'
        return s

    def setCurrentMove(self, move):
        self.cards = sorted(self.cards, key=lambda x: x.value)
        if(move.isOver):
            return
        if(move.playerMove == self): # player move is attackr
            self.__move(move)
            move.print_Move(self, True)
        else:
            self.__defense(move)
            move.print_Move(self, False)

    def __defense(self, move):
        if(move.isOver == True):
            return
        if(self.isBot):
            for card in self.aiGetCards():
                if(self.__checkAvailable(move, card)):
                    self.cards.remove(card)
                    move.add(self, card)
                    return
            self.__getCards(move)
        else:
            self.__userInput(move, False)

    def __move(self, move):
        if(self.isBot):
            for card in self.aiGetCards():
                if(card.suit == move.trumpCard.suit and len(move.cards) > 0):
                    continue
                if(self.__checkAvailable(move, card)):
                    move.add(self, card)
                    self.cards.remove(card)
                    return
            self.__moveOver(move)
        else: 
            self.__userInput(move, True)

    def __checkAvailable(self, move, moveCard):
        if(moveCard is None): 
            return False
        if(len(move.cards) == 0): 
            return True
        # If move
        if(move.playerMove == self):
            return any(x.name == moveCard.name for x in move.cards)
        # If defense
        cardForDefense = move.cards[len(move.cards)-1]
        # Find the higher card same suit
        if(moveCard.suit == cardForDefense.suit and moveCard.value > cardForDefense.value):
            return True
        if(move.trumpCard.suit != cardForDefense.suit and move.trumpCard.suit == moveCard.suit):
            return True
        return False

    def __getCards(self, move):
        move.moveOver()
        self.cards = self.cards + move.cards

    def __moveOver(self, move):
        move.moveOver()

    def __userInput(self, move, isMove):
        taketext = getText('TAKE')
        passtext = getText('PASS')

        currentActionName = getText('YOUR_TURN').format('\033[92m', self.name, '\033[00m') if isMove else getText('YOUR_DEFENSE').format('\033[91m', self.name, '\033[00m')
        spacer = '##########'
        if(isMove and len(move.cards) > 0): 
            print_ (getText('ENTER_COMMAND_FOR_END_MOVE').format(spacer, '\033[95m', passtext, '\033[00m'))
        elif(not isMove):
            print_ (getText('ENTER_COMMAND_FOR_TAKE_CARDS').format(spacer, '\033[95m', taketext, '\033[00m'))
        print_ (getText('SHOW_TRUMP_CARD').format(spacer, move.trumpCard.fullName()))
        print_ (getText('ENTER_CARD_NUMBER').format(spacer, currentActionName))
        while (True):
            Card.showCards(self.cards)
            cardNumber = input(': ')
            if(isMove and cardNumber == passtext and len(move.cards) > 1):
                self.__moveOver(move)
                return
            if(not isMove and cardNumber == taketext):
                self.__getCards(move)
                return
            card = self.__findCard(cardNumber)
            if(self.__checkAvailable(move, card) and move.add(self, card)):
                self.cards.remove(card)
                return
            else: print_ (getText('WRONG_MOVE'))

    def __findCard(self, cardNumber):
        try:
            cardNumber = int(cardNumber)
        except ValueError:
            return None

        for i in range(0, len(self.cards)):
            if(self.cards[i].number == cardNumber):
                return self.cards[i]
        return None

    def __aiGetMin(self, move, isTrump):
        cards = list(filter(lambda x: (x.suit == move.trumpCard.suit) == isTrump, self.cards))
        if(len(cards) == 0): return None
        return min(cards, key=lambda x: x.number)

    def aiGetCards(self):
        return sorted(self.cards, key=lambda x: x.value)

        

