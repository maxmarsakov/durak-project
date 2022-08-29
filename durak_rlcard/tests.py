# yes its a little bit hacky but it works
import sys
sys.path.insert(0,'.')

import rlcard
from rlcard.agents import RandomAgent
from env import DurakEnv
from agents import HumanAgent
from agents import SimpleAgent, SimpleLearningAgent, SimpleProbaAgent
import random


from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    reorganize,
    Logger,
    plot_curve,
)

def basic_dou_dizhu():
    env = rlcard.make(
        "doudizhu",
        config={
            'seed': 1,
        }
    )
    agents = [RandomAgent(num_actions=env.num_actions),RandomAgent(num_actions=env.num_actions),RandomAgent(num_actions=env.num_actions)]
    env.set_agents(agents)
    print(env.num_actions) # 2
    print(env.num_players) # 1
    print(env.state_shape) # [[2]]
    print(env.action_shape) # [None]
    trajectories, payoffs = env.run()
    print(payoffs)


def basic_human_test():
    env = DurakEnv()
    env.set_agents([HumanAgent(num_actions=env.num_actions),HumanAgent(num_actions=env.num_actions)])
    trajectories, payoffs = env.run()
    print(payoffs)
    

def basic_random_test():
    env = DurakEnv()
    env.set_agents([RandomAgent(num_actions=env.num_actions),RandomAgent(num_actions=env.num_actions)])
    print(env.num_actions) # 2
    print(env.num_players) # 1
    print(env.state_shape) # [[2]]
    print(env.action_shape) # [None]

    trajectories, payoffs = env.run()
    print(payoffs)

def basic_tournament_test():
    env = DurakEnv()
    set_seed(0)
    env.set_agents([RandomAgent(num_actions=env.num_actions),RandomAgent(num_actions=env.num_actions)])
    print( tournament(env,100)  )

def basic_blackjack():
    env = rlcard.make(
        "blackjack",
        config={
            'seed': 1,
        }
    )
    agents = [RandomAgent(num_actions=env.num_actions),RandomAgent(num_actions=env.num_actions)]
    env.set_agents(agents)
    print(env.num_actions) # 2
    print(env.num_players) # 1
    print(env.state_shape) # [[2]]
    print(env.action_shape) # [None]
    trajectories, payoffs = env.run()
    print(payoffs)

def basic_simple_tournament():
    # basic simple tournament vs random
    env = DurakEnv()
    set_seed(0)
    env.set_agents([SimpleAgent(num_actions=env.num_actions),RandomAgent(num_actions=env.num_actions)])
    print( tournament(env,1000)  )

def basic_simple_learning_tournament():
    # basic simple tournament vs random
    env = DurakEnv()
    device=get_device()
    learning_agent=SimpleLearningAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        mlp_layers=[64,64],
        device=device,
    )

    env.set_agents([learning_agent,RandomAgent(num_actions=env.num_actions)])
    print( tournament(env,1000) )


def basic_simple_proba_tournament():
    # basic simple tournament vs random
    env = DurakEnv()
    device=get_device()

    # simple callback is needed to determine 
    # when to use simple vs dqn strategy
    learning_agent=SimpleProbaAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        mlp_layers=[64,64],
        device=device,
        proba_at_start=0.1,
        proba_at_end=0.9,
    )

    env.set_agents([learning_agent,RandomAgent(num_actions=env.num_actions)])
    print( tournament(env,1000) )

def basic_simple_proba_threshold_tournament():
    # basic simple tournament vs random
    env = DurakEnv()
    device=get_device()

    # simple callback is needed to determine 
    # when to use simple vs dqn strategy
    learning_agent=SimpleProbaAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        mlp_layers=[64,64],
        device=device,
        proba_at_start=0.1,
        proba_at_end=0.9,
        threshold=5
    )

    env.set_agents([learning_agent,RandomAgent(num_actions=env.num_actions)])
    print( tournament(env,1000) )

if __name__ == "__main__":
    set_seed(0)
    #basic_simple_tournament()
    #basic_simple_learning_tournament()
    #basic_simple_proba_tournament()
    basic_simple_proba_threshold_tournament()
    #basic_human_test()
    #basic_blackjack()

