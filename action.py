# -*- coding: utf-8 -*-


class Action:
    def __init__(self, card=None, is_trump=False, take=False, bita=False, noop=False):
        self.card = card
        self.is_trump = is_trump
        self.take = take
        self.bita = bita