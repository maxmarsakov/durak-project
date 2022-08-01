# -*- coding: utf-8 -*-
''' Implement Durak Game class
'''
import functools
from heapq import merge
import numpy as np

import durak2 as dk


class Game:
    ''' Provide game APIs for env to run doudizhu and get corresponding state
    information.
    '''
    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 2
        self.allow_step_back = False

        # initialise game instance
        self.g=dk.Durak()

    def init_game(self):
        ''' Initialize players and state.
        Returns:
            dict: first state in one game
            int: current player's id
        '''
        self.g.newGame()
        current_player = self.g.getFirstAttacker()

        # initialize public variables
        self.winner_id = None
        self.history = []

        # get state of first player
        player_id = current_player
        self.state = self.get_state(player_id)

        return self.state, player_id

    def step(self, action):
        ''' Perform one draw of the game
        Args:
            action (str): specific action of doudizhu. Eg: '33344'
        Returns:
            dict: next player's state
            int: next player's id
        '''
        if self.allow_step_back:
            # TODO: don't record game.round, game.players, game.judger if allow_step_back not set
            pass

        # perfrom action
        current_player=self.g.getCurrentPlayer()
        self.g.playCard(current_player, action)

        if self.g.roundOver():
            # check winner
            if self.g.gameOver():
                self.winner_id = self.g.winner
            else:
                # new round, refil hands and set current player
                self.g.endRound() 
                # edge case
                if self.g.gameOver():
                    self.winner_id = self.g.winner

        next_id = self.g.getCurrentPlayer()
        # get next state
        state = self.get_state(next_id)
        self.state = state

        return state, next_id


    def get_state(self, player_id):
        ''' Return player's state
        Args:
            player_id (int): player id
        Returns:
            (dict): The state of the player
        '''
        
        state = self.g.getState(player_id)

        if self.is_over():
            actions = []
        else:
            if self.g.attacker == self.g.current_player:
                actions = self.g.getAttackOptions(self.g.current_player)
            else:
                actions = self.g.getDefendOptions(self.g.current_player)
        #state = player.get_state(self.round.public, others_hands, num_cards_left, actions)
        state['actions']=actions
        state['current_player']=self.g.current_player
        return state

    @staticmethod
    def get_num_actions():
        ''' Return the total number of abstract acitons
        Returns:
            int: the total number of abstract actions of doudizhu
        '''
        return 37

    def get_player_id(self):
        ''' Return current player's id
        Returns:
            int: current player's id
        '''
        return self.g.getCurrentPlayer()

    def get_num_players(self):
        ''' Return the number of players in doudizhu
        Returns:
            int: the number of players in doudizhu
        '''
        return self.num_players

    def is_over(self):
        ''' Judge whether a game is over
        Returns:
            Bool: True(over) / False(not over)
        '''
        if self.winner_id is None:
            return False
        return True

    """
    getters
    """
    def get_hand(self,player_id):
        return self.g.hand[player_id]

    def get_current_player(self):
        return self.g.getCurrentPlayer()

    # still not in use
    """
    def _get_others_current_hand(self, player):
        player_up = self.players[(player.player_id+1) % len(self.players)]
        player_down = self.players[(player.player_id-1) % len(self.players)]
        others_hand = merge(player_up.current_hand, player_down.current_hand, key=functools.cmp_to_key(doudizhu_sort_card))
        return cards2str(others_hand)
    """