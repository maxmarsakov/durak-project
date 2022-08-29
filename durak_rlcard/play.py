"""
play different models
"""
import os
import argparse
from turtle import numinput

import sys
# yes its a little bit hacky but it works
sys.path.insert(0,'.')

import rlcard
from agents import HumanAgent

from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)

from env import DurakEnv

def load_model(model_path, env=None, position=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif os.path.isdir(model_path):  # CFR model
        from rlcard.agents import CFRAgent
        agent = CFRAgent(env, model_path)
        agent.load()
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    elif model_path == 'simple':  # Random model
        from agents import SimpleAgent
        agent = SimpleAgent(num_actions=env.num_actions)
    else:  # A model in the model zoo
        from rlcard import models
        agent = models.load(model_path).agents[position]
    
    return agent

def play(args):

    # Check whether gpu is available
    device = get_device()
    env = DurakEnv()

    # Load models
    agents = [HumanAgent(num_actions=env.num_actions)]
    for position, model_path in enumerate(args.models):
        agents.append(load_model(model_path, env, position, device))
    env.set_agents(agents)
    trajectories, payoffs = env.run()
    print("winner score")
    print("Human player: {}/1".format(payoffs[0]))
    print("Agent: {}/1 ".format(payoffs[1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Play in RLCard")
   
    parser.add_argument(
        '--models',
        nargs='*',
        default=[
            'random',
        ],
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
    )
    parser.add_argument(
        '--num_games',
        type=int,
        default=2000,
    )

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    play(args)

