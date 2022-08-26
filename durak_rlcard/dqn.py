"""
main traning file for DQN agents
"""

from optparse import OptionParser
import os
import argparse

import torch
import time

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    reorganize,
    Logger,
    plot_curve,
)
from env import DurakEnv
from agents import SimpleAgent, SimpleLearningAgent, SimpleProbaAgent
import random
from collections import namedtuple

CustomArgs=namedtuple('CustomArgs',['agent','opponent','cuda','seed','num_episodes','num_eval_games','evaluate_every','save_every','log_dir'])

def train(args,env,agent,evaluate_vs=None):

    # Start training
    curr_time=None
    with Logger(args.log_dir) as logger:
        for episode in range(args.num_episodes):

            if args.agent == 'nfsp':
                agent.sample_episode_policy()

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            # Here, we assume that DQN always plays the first position
            # and the other players play randomly (if any)
            for ts in trajectories[0]:
                agent.feed(ts)

            if args.opponent=="self":
                # if playing against self, copy self as opponent
                env.set_agents([agent,agent])

            # Evaluate the performance. Play with random agents.
            if episode % args.evaluate_every == 0:
                prev_agents=env.agents
                if evaluate_vs is not None:
                    env.set_agents([agent,evaluate_vs])
                logger.log_performance(
                    env.timestep,
                    tournament(
                        env,
                        args.num_eval_games,
                    )[0]
                )
                if evaluate_vs is not None:
                    env.set_agents(prev_agents)
            
            if curr_time is None or ( (time.perf_counter()-curr_time) > 60 * args.save_every):
                # as well save the model
                save_path = os.path.join(args.log_dir, 'model.pth')
                torch.save(agent, save_path)
                curr_time=time.perf_counter()

        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, args.agent)

    # Save model
    save_path = os.path.join(args.log_dir, 'model.pth')
    torch.save(agent, save_path)
    print('Model saved in', save_path)

def parse_args_terminal():
    parser = argparse.ArgumentParser("DQN/NFSP example in RLCard")
 
    parser.add_argument(
        '--agent',
        type=str,
        default='dqn',
        choices=[
            'dqn',
            'nfsp',
            'simple_learning',
            'simple_proba',
            'simple_inverted'
        ],
    )
    
    parser.add_argument(
        '--opponent',
        type=str,
        default='random',
        choices=[
            'random',
            'simple',
            'self'
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
        '--num_episodes',
        type=int,
        default=5000,
    )
    parser.add_argument(
        '--num_eval_games',
        type=int,
        default=2000,
    )
    parser.add_argument(
        '--evaluate_every',
        type=int,
        default=100,
    )

    parser.add_argument(
        '--save_every',
        type=int,
        default=30,
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default='experiments/',
    )

    args = parser.parse_args()
    return args

def get_agent_opponent(env,args):
    agent,opponent=None,None

    if args.agent == 'dqn':
        from rlcard.agents import DQNAgent
        agent = DQNAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            mlp_layers=[64,64],
            device=device,
        )
    elif args.agent == 'nfsp':
        from rlcard.agents import NFSPAgent
        agent = NFSPAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            hidden_layers_sizes=[64,64],
            q_mlp_layers=[64,64],
            device=device,
        )
    elif args.agent == 'simple_learning':
        from agents import SimpleLearningAgent
        agent = SimpleLearningAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            mlp_layers=[64,64],
            device=device,
        )
    elif args.agent == 'simple_inverted':
        from agents import SimpleInvertedAgent
        agent = SimpleInvertedAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            mlp_layers=[64,64],
            device=device,
        )
    elif args.agent == 'simple_proba':
        from agents import SimpleProbaAgent
        agent = SimpleProbaAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            mlp_layers=[64,64],
            device=device,
            proba_at_start=0.1,
            proba_at_end=0.9,
        )
    
    # set opponent
    if args.opponent=='random':
        from rlcard.agents import RandomAgent
        opponent=RandomAgent(num_actions=env.num_actions)
    elif args.opponent=='simple':
        from agents import SimpleAgent
        opponent=SimpleAgent(num_actions=env.num_actions)
    elif args.opponent=='self':
        # copy agent
        opponent=agent

    return tuple([agent,opponent])

if __name__ == '__main__':

    args=parse_args_terminal()

    # Check whether gpu is available
    device = get_device()
    set_seed(args.seed)
    env = DurakEnv()

    agent,opponent=get_agent_opponent(env,args)    

    # Initialize the agents
    env.set_agents([agent,opponent])
    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda

    train(args,env,agent)