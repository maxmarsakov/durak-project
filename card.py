from console import print_

class Card:
    def __init__(self, name, suit, number, value):
        self.name = name
        self.suit = suit
        self.number = number
        self.value = value

    def fullName(self):
        if(self.suit in ['♦','♥']): color = '\033[91m'
        else: color = '\033[30m'
        return f'\033[47m {color}{self.suit}\033[00m\033[47m\033[30m {self.name} \033[00m'

    @staticmethod
    def showCards(cards):
        cardLength = len(cards)
        print_(' ', end='')
        for x in range(0, cardLength):
            card = cards[x]
            separator = '  '
            if(x == cardLength-1): separator = ''
            print_(f'\033[96m{card.number}\033[00m.{card.fullName()}{separator}', end='')  