import numpy as np
from agents.simple_agent import SimpleAgent
from rlcard.agents import DQNAgent


class SimpleInvertedAgent(DQNAgent):
    ''' 
    SimpleLearningAgent is the agent that chooses uses simple agent strategy
    and mixes it with DQNAgent, at the very end of the game
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
        device=None):
        ''' Initilize the random agent
        Args:
            num_actions (int): The size of the ouput action space
        '''
        super().__init__(replay_memory_size, replay_memory_init_size,  update_target_estimator_every, discount_factor, epsilon_start,\
              epsilon_end,  epsilon_decay_steps,  batch_size, num_actions, state_shape, train_every, mlp_layers,  learning_rate, device)
        #self.use_raw = False
        #self.num_actions = num_actions

    def step(self,state):
        ''' Predict the action given the curent state in gerenerating training data.
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        raw=state['raw_obs']
        deckSize=raw['deckSize']
        #print(deckSize)
        if deckSize>0:
            #simple
            return super().step(state)
        # dqna
        return SimpleAgent.simple_strategy_step(state)
        

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
           
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        raw=state['raw_obs']
        deckSize=raw['deckSize']
        if deckSize>0:
            #dqna
            return super().eval_step(state)

        return SimpleAgent.simple_strategy_step(state), {}
        
        