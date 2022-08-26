import numpy as np
from env import decode_action
from .human_agent import format_suit_card, suit_to_string

STOP_SUIT=-1

class SimpleAgent(object):
    ''' SimpleAgent is the agent that chooses the lowest card
    '''

    def __init__(self, num_actions):
        ''' Initilize the random agent
        Args:
            num_actions (int): The size of the ouput action space
        '''
        self.use_raw = False
        self.num_actions = num_actions

    def step(self,state):
        ''' Predict the action given the curent state in gerenerating training data.
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        return SimpleAgent.simple_strategy_step(state)

    @staticmethod
    def simple_strategy_step(state):
        """
        simple strategy helper
        """
        if len(state['legal_actions']) == 1:
            return list(state['legal_actions'].keys())[0]
        trumpSuit=state['raw_obs']['trumpSuit']
        
        legal_decoded_actions=[(k,decode_action(k)) for k in dict(state['legal_actions']) ]
        non_trump_cards=[(k,a) for k,a in legal_decoded_actions if a.suit not in (trumpSuit,STOP_SUIT)]

        if len(non_trump_cards)>0:
            m=min(non_trump_cards, key=lambda x: x[1])
            return m[0]
        trump_cards=[(k,a) for k,a in legal_decoded_actions if a.suit==trumpSuit]
        m=min(trump_cards, key=lambda x: x[1])
        return m[0]

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
           
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        return self.step(state), {}