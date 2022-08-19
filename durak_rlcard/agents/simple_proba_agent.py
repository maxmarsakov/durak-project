import numpy as np
from agents.simple_agent import SimpleAgent
from rlcard.agents import DQNAgent


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
        use_strategy_callback=None
        ):
        ''' Initilize the random agent
        Args:
            num_actions (int): The size of the ouput action space
        '''
        super().__init__(replay_memory_size, replay_memory_init_size,  update_target_estimator_every, discount_factor, epsilon_start,\
              epsilon_end,  epsilon_decay_steps,  batch_size, num_actions, state_shape, train_every, mlp_layers,  learning_rate, device)
        #self.use_raw = False
        
        if use_strategy_callback is None:
            raise Exception("must set use_strategy_callback for this agent!")

        # use strategy callback is called in step, to determine when to use 
        # simple strategy versus when to use dqna strategy (may be probabalistic or not)
        self.use_strategy_callback=use_strategy_callback

    def step(self,state):
        ''' Predict the action given the curent state in gerenerating training data.
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        if self.use_strategy_callback(state)=='dqn':
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
        if self.use_strategy_callback(state)=='dqn':
            # dqna
            return super().eval_step(state)
        #simple
        return SimpleAgent.simple_strategy_step(state), {}