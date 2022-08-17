import numpy as np


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

    @staticmethod
    def step(state):
        ''' Predict the action given the curent state in gerenerating training data.
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        # TODO

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
           
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        # TODO
        return self.step(state), {}