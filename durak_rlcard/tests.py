import rlcard
from rlcard.agents import RandomAgent
from env import DurakEnv

def basic_random_test():
    env = DurakEnv()
    env.set_agents([RandomAgent(num_actions=env.num_actions),RandomAgent(num_actions=env.num_actions)])
    print(env.num_actions) # 2
    print(env.num_players) # 1
    print(env.state_shape) # [[2]]
    print(env.action_shape) # [None]

    trajectories, payoffs = env.run()

if __name__ == "__main__":
    basic_random_test()

