"""
this file contains main loops for the game 
needed for training, as well as evaluation of the game
"""
import argparse
import numpy as np
import agents
from collections import Counter
from deck import DeckType
from player import Player
# after refactoring change
#from ai_player import Player
from ai_durak import Durak
from move import Move

# game wrapper for Durak
class Game():

    def __init__(self,agents):
        # instantiate durak 
        # TODO - modify PLAYER functionality to support agents
        self.durak = Durak(agents,DeckType.Card36, 6)
 
        self.agents = agents
        self.winner = None
        # state varibles
        # self.deck
        # seld.hands[]
        # self.trash
        # self.move (AKA table)

    def getState(self, playerNumber:int):
        """
        this function returns the state of the game, for the 
        player which is identified by playerNumber
        """
        pass

    def getAttackActions(self, player):
        """
        TODO
        """
        pass

    def getDefendActions(self,player):
        """
        TODO - add valid action for the defender
        """
        pass

    def roundOver(self, move):
        return move.isOver

    def gameOver(self):
        # This function not really decides the looser
        loser = self.durak.checkLoserExist()
        gameOver = loser[0]
        if gameOver:
            self.winner = [player for player in self.agents if player != loser][0]
        return gameOver
        
    def endRound(self):
        self.durak.handOverCards()

    def attack_new(self, attacker, move):
        
        actions = self.getAttackActions(attacker)
        card = attacker.choose_action(actions, self)
        attacker.applyAttackAction(card,move)

    def defend_new(self, defender, move):
        actions = self.getDefendActions(defender)
        card = defender.choose_action(actions, self)
        defender.applyDefenseAction(card,move)

    def attack(self, attacker, move):
        """
        performs an attacker action, based on attacker policy
        TODO: change for something like
        getAttackOptions()
        filter(self.hand[payer]), which are according to the move
        and then,attacker may expand via (attacker.chooseAction(actions, self,game))
        """
        attacker.setCurrentMove(move)

    def defend(self, defender, move):
        """
        performs an defender action
        TODO: the same as in the attack, but for defend
        """
        defender.setCurrentMove(move)

    def play(self):
        """
        plays one game, using provided agent
        returns winning player
        """
        self.durak.fillDeck()
        self.durak.shuffleDeck()
        self.durak.defineTrump()
        self.durak.handOverCards()
        move = None
        attacker, defender = self.durak.nextPlayers(move)

        while True:
            move = Move(self.durak.trumpCard, attacker, defender)

            while True:
                # attack
                self.attack(attacker, move)
                self.defend(defender, move)
                if self.roundOver(move) or self.gameOver():
                    break
                    
            if self.gameOver():
                break

            self.endRound()
            # Edge case: last round, the defender ran out of cards & the attacker got under
            # 6 cards. The attacker took the rest of the deck, so the defender (new attacker)
            #if self.gameOver():
            #    break
            attacker, defender = self.durak.nextPlayers(move)

        return self.winner


def parseArgs():
    parser = argparse.ArgumentParser(
        description='Play a two-player game of Durak against a random-policy opponent.')
    parser.add_argument('-a', '--agent', type=str, default='simple',
                        choices=['human', 'random', 'simple', 'reflex', 'minimax'], help="Agent type")
    parser.add_argument('-o', '--opponent', type=str, default='simple',
                        choices=['human', 'random', 'simple', 'reflex', 'minimax'], help="Opponent type")
    # parser.add_argument('-v', '--verbose', type=int, default=1,
    #                     choices=[0, 1, 2], help="Verbosity of prompts")
    parser.add_argument('-n', '--numGames', type=int, default=100,
                        help="Number of games to play")
    parser.add_argument('-t', '--train', action='store_true', help='Train the AI')
    return parser.parse_args()


def getAgent(agentType, playerNum):
    if agentType == 'human':
        return agents.HumanAgent("human",playerNum)
    elif agentType == 'random':
        return agents.RandomAgent("random")
    elif agentType == 'simple':
        return agents.SimpleAgent("simple")
    elif agentType == 'reflex':
        return agents.ReflexAgent("reflex",playerNum)
    elif agentType == 'minimax':
        return agents.MinimaxAgent("minimax", playerNum)


def play(agents, num_games=1):
    """
    play game, print stats
    """
    winners = Counter()
    for _ in range(num_games):
        g = Game(agents)
        winner = g.play()
        print("GAME DONE")
        winners[winner] += 1

    for j, player in enumerate(agents):
        # TODO: add names for agent winners
        print(f"win rate of agent {j} is {winners[player]/num_games}")
        


def train():
    """
    TODO
    """
    pass

if __name__ == "__main__":

    args = parseArgs()
    # two player scenario
    #agents = [getAgent(args.agent,0),getAgent(args.opponent, 1)]
    agents = [Player("diego"), Player('bot', True)]

    if args.train:
        train(agents, args.numGames)
    else:
        play(agents, args.numGames)
