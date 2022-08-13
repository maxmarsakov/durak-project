import math
from xml.dom import minicompat
import base.durak2 as dk
import numpy as np


def readIntegerInRange(minimum, maximum, prompt=''):
    while True:
        text = input(prompt)
        try:
            num = int(text)
            # max fix
            if minimum == maximum:
                maximum = maximum+1
                
            if num in range(minimum, maximum):
                return num
            else: 
                print("Out of range [%s, %s), try again" % (minimum, maximum))
        except ValueError:
            print("Not an int, try again")


def logisticValue(weights, features):
    z = np.dot(weights, features)
    return 1.0 / (1 + math.exp(-z))


### FEATURE EXTRACTION


def getNumOpponentMoves(state):
    N = len(state['unseen'])
    n = state['opponentHandSize'] - len(state['knownOpponentHand'])
    K = 0
    nOpponentMoves = 0

    if state['isAttacker'] and len(state['table']) > 0:
        topCard = state['table'].getTopCard()
        nOpponentMoves += len([c for c in state['knownOpponentHand'].getCardsForSuit(topCard.suit) if c.rank > topCard.rank])
        K += len([c for c in state['unseen'].getCardsForSuit(topCard.suit) if c.rank > topCard.rank])
        if topCard.suit != state['trumpSuit']:
            nOpponentMoves += len(state['knownOpponentHand'].getCardsForSuit(state['trumpSuit']))
            K += len(state['unseen'].getCardsForSuit(state['trumpSuit']))
        if N > 0:
            nOpponentMoves += float(n * K) / N
    elif state['isAttacker'] and len(state['table']) == 0:
        nOpponentMoves = state['opponentHandSize']
    elif not state['isAttacker']:
        for rank in dk.Card.RANKS:
            if rank in state['table'].seenRanks:
                nOpponentMoves += len(state['knownOpponentHand'].getCardsForRank(rank))
                K += len(state['unseen'].getCardsForRank(rank))
        if N > 0:
            nOpponentMoves += float(n * K) / N

    return nOpponentMoves


def getNumValidMoves(state):
    nValidMoves = 0
    if state['isAttacker']:
        for rank in state['table'].seenRanks:
            nValidMoves += len(state['hand'].getCardsForRank(rank))
    return nValidMoves


def getAverageRanks(hand):
    averages = []
    for suit in dk.Card.SUITS:
        sumRanks = sum(c.rank for c in hand.getCardsForSuit(suit))
        nCards = len(hand.getCardsForSuit(suit))
        if sumRanks == 0:
            averages.append(0)
        else:
            averages.append(float(sumRanks) / nCards)
    return averages


def extractFeatures(state):
    # nValidMoves = getNumValidMoves(state)
    # nOpponentMoves = getNumOpponentMoves(state)
    avgRanks = getAverageRanks(state['hand'])
    cardsPerRank = [len(state['hand'].getCardsForRank(rank)) for rank in dk.Card.RANKS]
    cardsPerSuit = [len(state['hand'].getCardsForSuit(suit)) for suit in dk.Card.SUITS]
    avgRanksTrash = getAverageRanks(state['trash'])
    cardsPerRankTrash = [len(state['trash'].getCardsForRank(rank)) for rank in dk.Card.RANKS]
    cardsPerSuitTrash = [len(state['trash'].getCardsForSuit(suit)) for suit in dk.Card.SUITS]
    nTrumpCards = len(state['hand'].getCardsForSuit(state['trumpSuit']))
    nHandCards = [len(state['hand'])]
    nOpponentsHandCards = [state['opponentHandSize']]
    nCardsInDeck = [state['deckSize']]
    # to check if knowing the cards of the opponent hand
    # avgRanksOpponent = getAverageRanks(state['knownOpponentHand'])
    # cardsPerRankOpponent = [len(state['knownOpponentHand'].getCardsForRank(rank)) for rank in dk.Card.RANKS]
    # cardsPerSuitOpponent= [len(state['knownOpponentHand'].getCardsForSuit(suit)) for suit in dk.Card.SUITS]
    return np.array(avgRanks + cardsPerRank + cardsPerSuit + avgRanksTrash + cardsPerRankTrash + cardsPerSuitTrash +
                    nHandCards + [nTrumpCards, 1.0] + nOpponentsHandCards + nCardsInDeck)
    # return np.array(avgRanks + cardsPerRank + cardsPerSuit + [nTrumpCards, 1.0])

# NUM_FEATURES = 4 + 9 + 4 + 2
NUM_FEATURES = 4 + 9 + 4 + 4 + 9 + 4 + 1 + 1 + 2