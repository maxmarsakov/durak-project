import argparse
import pickle
import numpy as np

import base.durak2 as dk
from base.console import print_, format_suit_card, print_round_info
import base.util as util

import agent as agt

from collections import namedtuple
Reward = namedtuple('Reward', 'win_game loose_game win_round loose_round default')

gargs = None

def parseArgs():
    parser = argparse.ArgumentParser(
        description='Play a two-player game of Durak against a random-policy opponent.')
    parser.add_argument('-a', '--agent', type=str, default='minimax',
                        choices=['human', 'random', 'simple', 'reflex', 'minimax','qagent'], help="Agent type")
    parser.add_argument('-o', '--opponent', type=str, default='simple',
                        choices=['human', 'random', 'simple', 'reflex', 'minimax','qagent'], help="Opponent type")
    parser.add_argument('-v', '--verbose', action='store_true', help='verbosity')
    parser.add_argument('-n', '--numGames', type=int, default=1,
                        help="Number of games to play")
    parser.add_argument('-t', '--train', action='store_true', help='Train the AI')
    #parser.add_argument('-m', '--method', type=str, choices=['TD', 'Q'], default='TD', help='Choose the training method: TD or Qlearning')
    return parser.parse_args()

# hyper parameters for learning
DISCOUNT=1
ETA=1e-1

def getAgent(agentType, playerNum):
    if agentType == 'human':
        return agt.HumanAgent(playerNum)
    elif agentType == 'random':
        return agt.RandomAgent()
    elif agentType == 'simple':
        return agt.SimpleAgent()
    elif agentType == 'reflex':
        return agt.ReflexAgent(playerNum)
    elif agentType == 'minimax':
        return agt.MinimaxAgent(playerNum)
    elif agentType == 'qagent':
        return agt.ApproximateQAgent(playerNum)

"""
different methods for training our agents
TDupdate - temporal difference
"""

def TDUpdate(state, nextState, reward, w, eta=ETA, discount=DISCOUNT, action=None, possible_actions=None):
    features = util.extractFeatures(state)
    value = util.logisticValue(w, features)
    #print("value", value)
    residual = reward - value
    if nextState is not None:
        nextFeatures = util.extractFeatures(nextState)
        residual += util.logisticValue(w, nextFeatures)
    gradient = value * (1 - value) * features
    newWeights = w + eta * residual * gradient
    return newWeights


def train(args, update_func=TDUpdate, reward: Reward=None):
    """
    method is the function to update : tdupdate or qupdate, 
    """
    print("Training process start: ", update_func.__name__, "rewards", reward)
    w_atk = np.random.normal(0, 1e-2, (util.NUM_FEATURES,))
    w_def = np.random.normal(0, 1e-2, (util.NUM_FEATURES,))
    w_atk[-1] = 0
    w_def[-1] = 0

    agents = [getAgent(args.agent, 0), getAgent(args.agent, 1)]
    for agent in agents:
        agent.setAttackWeights(w_atk)
        agent.setDefendWeights(w_def)

    g = dk.Durak()
    for i in range(args.numGames):
        attacker = g.getFirstAttacker()
        defender = int(not attacker)
        while True:
            preAttack = None
            preDefend = None
            defend_action=None
            attack_action=None
            while True:
                preAttack = g.getState(attacker)
                attack_action = attack(g, attacker, agents[attacker])
                postAttack = g.getState(defender)
                if g.roundOver():
                    # TODO: add rewards for successful round
                    break
                elif preDefend is not None:
                    w_def = update_func(preDefend, postAttack, reward.default, w_def, action=defend_action)
                    for agent in agents:
                        agent.setDefendWeights(w_def)

                preDefend = postAttack
                defend_action = defend(g, defender, agents[defender])
                postDefend = g.getState(attacker)
                if g.roundOver():
                    # TODO: add rewards for successful round
                    break
                else:
                    w_atk = update_func(preAttack, postDefend, reward.default, w_atk, action=attack_action)
                    for agent in agents:
                        agent.setAttackWeights(w_atk)

            if g.gameOver():
                if g.isWinner(attacker):
                    w_atk = update_func(g.getState(attacker), None, reward.win_game, w_atk, action=attack_action)
                    w_def = update_func(g.getState(defender), None, reward.loose_game, w_def, action=defend_action)
                else:
                    w_def = update_func(g.getState(defender), None, reward.win_game, w_def, action=defend_action)
                    w_atk = update_func(g.getState(attacker), None, reward.loose_game, w_atk, action=attack_action)
                for agent in agents:
                    agent.setAttackWeights(w_atk)
                    agent.setDefendWeights(w_def)
                break

            g.endRound()

            # Edge case, the defender from the last round won
            if g.gameOver():
                w_def = update_func(g.getState(defender), None, reward.win_game, w_def, action=defend_action)
                w_atk = update_func(g.getState(attacker), None, reward.loose_game, w_atk, action=attack_action)
                for agent in agents:
                    agent.setDefendWeights(w_def)
                    agent.setAttackWeights(w_atk)
                break
            else:
                w_def = update_func(preDefend, g.getState(defender), reward.default, w_def, action=defend_action)
                w_atk = update_func(preAttack, g.getState(attacker), reward.default, w_atk, action=attack_action)
                for agent in agents:
                    agent.setDefendWeights(w_def)
                    agent.setAttackWeights(w_atk)

            attacker = g.attacker
            defender = int(not attacker)

        if i % 50 == 0:
            print('Training iteration: %d / %d' % (i, args.numGames))

            # save weights partially
            with open('%s_attack_%d.bin' % (args.agent, i), 'wb') as f_atk:
                pickle.dump(w_atk, f_atk)
            with open('%s_defend_%d.bin' % (args.agent, i), 'wb') as f_def:
                pickle.dump(w_def, f_def)

            # Evaluation stage
            randomAgent = agt.RandomAgent()
            simpleAgent = agt.SimpleAgent()
            winCounts = {'random': 0, 'simple': 0}
            numGamesSim = 100
            for j in range(numGamesSim):
                winVsRandom = play(dk.Durak(), [randomAgent, agents[0]])
                winVsSimple = play(dk.Durak(), [simpleAgent, agents[0]])
                winCounts['random'] += winVsRandom
                winCounts['simple'] += winVsSimple

            print("win counts vs random", winCounts['random']/numGamesSim)
            print("win counts vs simple", winCounts['simple']/numGamesSim)
            with open('results.csv', 'a') as f:
                row = [i, winCounts['random']/numGamesSim, winCounts['simple']/numGamesSim]
                #row.extend(w_atk)
                #row.extend(w_def)
                np.savetxt(f, np.array(row)[:, None].T, delimiter=',', fmt='%.4e')    

        g.newGame()

    with open('%s_attack.bin' % args.agent, 'wb') as f_atk:
        pickle.dump(w_atk, f_atk)
    with open('%s_defend.bin' % args.agent, 'wb') as f_def:
        pickle.dump(w_def, f_def)

    

    return w_atk, w_def


def attack(g, playerNum, agent):
    actions = g.getAttackOptions(playerNum)
    card = agent.getAttackCard(actions, g)
    if gargs.verbose:
        print("attack card is", card)
    g.playCard(playerNum, card)
    return card


def defend(g, playerNum, agent):
    actions = g.getDefendOptions(playerNum)
    card = agent.getDefendCard(actions, g)
    g.playCard(playerNum, card)
    return card


    
def play(g, agents):
    attacker = g.getFirstAttacker()
    defender = int(not attacker)
    is_verbose = gargs.verbose or gargs.agent == "human" or gargs.opponent == "human"
    rounds = 0
    while True:
        if is_verbose:
            print_('# cards left: ', len(g.deck))
        while True:
            if is_verbose:
                print_('Trump suit: ', format_suit_card(dk.Card.SUITS[g.trumpCard.suit]) )
                print("====== attacker action =====")
            attack(g, attacker, agents[attacker])
            # print round info
            if is_verbose:
                print_round_info(g)
            if g.roundOver():
                break
            if is_verbose:
                print("====== defender action =====")
            defend(g, defender, agents[defender])
            # print round info
            if is_verbose:
                print_round_info(g)
            if g.roundOver():
                break
            rounds+=1

        if g.gameOver():
            break
        g.endRound()

        # Edge case: last round, the defender ran out of cards & the attacker got under
        # 6 cards. The attacker took the rest of the deck, so the defender (new attacker)
        # has 0 cards in his hand.
        if g.gameOver():
            break

        attacker = g.attacker
        defender = int(not attacker)

    return g.winner


def main(args):
    global gargs
    winCounts = [0, 0]
    agents = [None, None]
    agents[0] = getAgent(args.agent, 0)
    agents[1] = getAgent(args.opponent, 1)

    g = dk.Durak()
    is_verbose = gargs.verbose or gargs.agent == "human" or gargs.opponent == "human"
    for i in range(args.numGames):
        if is_verbose:
            print('=============== Game %d ===================' % (i))
        winner = play(g, agents)
        winCounts[winner] += 1
        print('Game %d winner: %d' % (i, winner))
        g.newGame()
    print('Win percentages:')
    print('Agent: %d/%d' % (winCounts[0], args.numGames))
    print('Opponent: %d/%d' % (winCounts[1], args.numGames))

def get_reward(method='TD'):
    if method=='Q':
        return Reward(100,0,1,0,0)
    elif method=='TD':
        return Reward(1,0,0,0,0)

if __name__ == '__main__':
    args = parseArgs()
    gargs = args

    if args.train and args.agent in ['reflex','minimax','qagent']:
        method = TDUpdate
        reward = get_reward('TD')
        print(reward)
        train(args, method, reward)
    else:
        main(args)