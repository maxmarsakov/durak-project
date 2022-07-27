# -*- coding: utf-8 -*-
from collections import Counter
from copy import deepcopy
from enum import Enum

from action import Action


class CardRank(Enum):
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13
    ace = 14

class State:
    def __init__(self, cards, deck, trump, bita, is_defense, move, has_opponent_pass):
        self.cards = cards
        self.trump = trump
        self.deck = deck
        self.bita = bita
        self.move = move
        self.has_opponent_pass = has_opponent_pass
        self.is_defense = is_defense
        self.deck_length = len(deck.cards)
        self.bita_length = len(bita)
        self.card_dict = self.count_cards(cards)
        self.bita_dict = self.count_cards(bita)
        self.num_of_cards = len(cards)
        self.unseen_cards()
        self.count_trumps()

    def count_trumps(self):
        self.num_of_trumps = 0
        for card in self.cards:
            if card.suit == self.trump:
                self.num_of_trumps += 1
    def unseen_cards(self):
        self.unseen_dict = dict()
        for i in CardRank:
            self.unseen_dict[i] = 4 - self.bita_dict[i] - self.card_dict[i]

    def count_cards(self, cards):
        card_dict = Counter()
        for card in cards:
            card_dict[card.value] += 1
        return card_dict

    def get_possible_actions(self):
        actions = list()
        if self.has_opponent_pass:
            actions.append(Action(noop=True))
            return actions
        for card in self.cards:
            if self.__checkAvailable(self.move, card):
                actions.append(Action(card, card.suit == self.trump))
        if self.is_defense:
            actions.append(Action(take=True))
        if not self.is_defense and len(self.move.cards) != 0:
            actions.append(Action(bita=True))
        return actions
        
    def get_next_state(self, action):
        # move should have been changed deck shouldn't
        if not (action.bita or action.take):
            new_move = deepcopy(self.move).add(None, action.card)
            new_cards = deepcopy(self.cards).remove(action.card)
            return State(new_cards, self.deck, self.trump, self.bita, self.is_defense, new_move,
                         self.has_opponent_pass)
        if action.bita or action.noop:
            new_bita = deepcopy(self.bita)
            for card in self.move.cards:
                new_bita.append(card)
            new_cards = deepcopy(self.cards)
            new_deck = deepcopy(self.deck)
            for i in range(len(self.deck.cards)):
                if len(new_cards) >= 6:
                    break
                new_cards.append(new_deck.cards[0])
                new_deck.pop(0)
            new_cards = sorted(new_cards, key=lambda x: x.value)
            return State(new_cards, new_deck, self.trump, new_bita, self.is_defense, list(),
                         self.has_opponent_pass)
        if action.take:
            new_cards = deepcopy(self.cards)
            for card in self.move.cards:
                new_cards.append(card)
            new_cards = sorted(new_cards, key=lambda x: x.value)
            return State(new_cards, self.deck, self.trump, self.bita, self.is_defense, list(),
                         self.has_opponent_pass)

    def __checkAvailable(self, move, moveCard):
        if (moveCard is None):
            return False
        if (len(move.cards) == 0):
            return True
        # If move
        if (not self.is_defense):
            return any(x.name == moveCard.name for x in move.cards)
        # If defense
        cardForDefense = move.cards[len(move.cards) - 1]
        # Find the higher card same suit
        if (moveCard.suit == cardForDefense.suit and moveCard.value > cardForDefense.value):
            return True
        if (move.trumpCard.suit != cardForDefense.suit and move.trumpCard.suit == moveCard.suit):
            return True
        return False