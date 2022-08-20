import numpy as np
from agents.simple_agent import SimpleAgent
from rlcard.agents import DQNAgent

TOTAL_CARDS=36
NUM_CARDS_AT_START=24
import random

class SimpleProbaAgent(DQNAgent):
    ''' 
    SimpleLearningAgent is the agent that chooses uses simple agent strategy
    and mixes it with DQNAgent, according to coin flipper callback function
    '''

    def __init__(self,
        replay_memory_size=20000,
        replay_memory_init_size=100,
        update_target_estimator_every=1000,
        discount_factor=0.99,
        epsilon_start=1.0,
        epsilon_end=0.1,
        epsilon_decay_steps=20000,
        batch_size=32,
        num_actions=2,
        state_shape=None,
        train_every=1,
        mlp_layers=None,
        learning_rate=0.00005,
        device=None,
        # proba parameters, linear probability transition
        proba_at_start=0.1, # the probability to use dqn at start
        proba_at_end=0.9, # the probabilty top use dqn at end
        threshold=None # if threshold is set, the probabilities are adjusted according to decksize
        ):
        ''' Initilize the random agent
        Args:
            num_actions (int): The size of the ouput action space
        '''
        super().__init__(replay_memory_size, replay_memory_init_size,  update_target_estimator_every, discount_factor, epsilon_start,\
              epsilon_end,  epsilon_decay_steps,  batch_size, num_actions, state_shape, train_every, mlp_layers,  learning_rate, device)
    
        self.proba_at_start=proba_at_start
        self.proba_at_end=proba_at_end
        self.threshold=threshold

    def use_strategy(self,state):
        """
        given state, and other parameters this function 
        determines when to use dqna vs simple
        it uses linear approximation to transition between dqn and simple strate
        """ 
        cards_left=state['raw_obs']['deckSize']
        coin = random.random()
        if self.threshold is not None:
            if cards_left >= self.threshold:
                # start game
                return 'dqn' if coin < self.proba_at_start else 'simple'
            return 'dqn' if coin < self.proba_at_end else 'simple'

        #(TOTAL_CARDS-(TOTAL_CARDS-NUM_CARDS_AT_START)  = NUM_CARDS_AT_START
        slope=(self.proba_at_end-self.proba_at_start)/NUM_CARDS_AT_START
        intercept=self.proba_at_end-slope*TOTAL_CARDS
        proba_use_dqn=slope*(TOTAL_CARDS-cards_left)+intercept

        if coin < proba_use_dqn:
            return "dqn"
        return "simple"

    def step(self,state):
        ''' Predict the action given the curent state in gerenerating training data.
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        if self.use_strategy(state)=='dqn':
            # dqna
            return super().step(state)
        #simple
        return SimpleAgent.simple_strategy_step(state)


    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
           
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        if self.use_strategy(state)=='dqn':
            # dqna
            return super().eval_step(state)
        #simple
        return SimpleAgent.simple_strategy_step(state), {}