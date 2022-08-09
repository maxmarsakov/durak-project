import rlcard
from rlcard.agents import RandomAgent
from env import DurakEnv
from human_agent import HumanAgent

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

if __name__ == "__main__":
    #basic_random_test()
    #basic_human_test()
    basic_blackjack()

