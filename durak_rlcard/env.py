"""
durak env for rlcard env
"""
from matplotlib.pyplot import table
import numpy as np
from collections import OrderedDict, Counter

from rlcard.envs import Env
from game import Game
from base.durak2 import Card

DEFAULT_GAME_CONFIG = {
        'game_num_players': 2,
        'game_num_decks': 1,
        'allow_step_back': False,
        'seed': 1
        }
TOTAL_CARDS = 36

class DurakEnv(Env):
    ''' DurakEnv Environment
    '''

    def __init__(self, config=DEFAULT_GAME_CONFIG):
        ''' Initialize the durak environment
        '''

        self.name = 'durak'
        self.game = Game()
        super().__init__(config)
        # TODO recalc state shape
        self.state_shape = [[229], [901], [901]]

        # add special action
        self.action_shape = [[TOTAL_CARDS+1] for _ in range(self.num_players)]

    def _get_legal_actions(self):
        ''' Get all legal actions for current state
        Returns:
            legal_actions (list): a list of legal actions' id
        '''
        legal_actions = self.game.state['actions']
        
        legal_actions = dict([ (self._compute_action_id(action),action) for action in legal_actions])
        #print(legal_actions)
        return legal_actions
    
    def _compute_action_id(self, action):
        if action.suit==-1:
            return 36
        action_id = action.suit*9+action.rank-6
        #print(action, action_id)
        return action_id
    

    def _extract_state(self, state):
        ''' Encode state
        Args:
            state (dict): dict of original state
        '''
        current_hand = _cards2array(state['hand'])
        others_hand = _cards2array(state['knownOpponentHand'])
        isAttacker = state['isAttacker']
        unseenCards = _cards2array(state['unseen'])
        table = _cards2array(state['table'])
        deckSize = state['deckSize']
        opponentHandSize = state['opponentHandSize']
        trumpSuit = _one_hot_index(state['trumpSuit'],4)
        trash = _cards2array(state['trash'])
        unseen = _cards2array(state['unseen'])

        obs = np.concatenate((current_hand,
                            others_hand,
                            [isAttacker],
                            unseenCards,
                            table,
                            [deckSize],
                            [opponentHandSize],
                            trumpSuit,
                            trash,
                            unseen
                            ))

        extracted_state = OrderedDict({'obs': obs, 'legal_actions': self._get_legal_actions()})
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in state['actions']]
        extracted_state['action_record'] = self.action_recorder
        return extracted_state
            
    def get_payoffs(self):
        ''' Get the payoffs of players. Must be implemented in the child class.
        Returns:
            payoffs (list): a list of payoffs for each player
        '''
        if self.game.winner_id is None:
            # should not happen
            return (0,0)
        payoffs = [0,0]
        payoffs[self.game.winner_id]=1
        return tuple(payoffs)
        

    def _decode_action(self, action_id):
        ''' Action id -> the action in the game. Must be implemented in the child class.
        Args:
            action_id (int): the id of the action
        Returns:
            action (string): the action that will be passed to the game engine.
        '''
        if (action_id==36):
            return Card(-1,-1)
        suit=action_id//9
        rank=action_id%9+6
        card = Card(suit,rank)
        return card


    def get_perfect_information(self):
        ''' Get the perfect information of the current state
        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        #state['hand_cards_with_suit'] = [self._cards2str_with_suit(player.current_hand) for player in self.game.players]
        state['hand_cards'] = [self.game.get_hand(0),self.game.get_hand(1)]
        # trace is table
        state['table'] = self.game.state['table']
        state['current_player'] = self.game.get_current_player()
        state['legal_actions'] = self.game.state['actions']
        return state

    def get_action_feature(self, action):
        ''' For some environments such as DouDizhu, we can have action features
        Returns:
            (numpy.array): The action features
        '''
        return _one_hot(self._decode_action(action))

Card2Column = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7,
               'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}

NumOnes2Array = {0: np.array([0, 0, 0, 0]),
                 1: np.array([1, 0, 0, 0]),
                 2: np.array([1, 1, 0, 0]),
                 3: np.array([1, 1, 1, 0]),
                 4: np.array([1, 1, 1, 1])}

def _one_hot(card):
    # gets one card, returns one hot
    base = np.zeros((4,9), dtype=np.int8)
    has_special=[0]
    if card.suit == -1: # special card:
        has_special=[1]
        return np.concatenate([base.flatten('F'),has_special])
    base[card.suit][card.rank-6] = 1
    return np.concatenate([base.flatten('F'),has_special])

def _cards2array(cards):
    base = np.zeros((4,9), dtype=np.int8)
    has_special=[0]
    for card in cards:
        if (card.suit == -1):
            has_special=[1]
        else:
            base[card.suit][card.rank-6] = 1
    return np.concatenate([base.flatten('F'),has_special])


def _one_hot_index(index,max_vals):
    one_hot = np.zeros(max_vals,int)
    one_hot[index]=1
    return one_hot

"""
def _get_one_hot_array(num_left_cards, max_num_cards):
    one_hot = np.zeros(max_num_cards, dtype=np.int8)
    one_hot[num_left_cards - 1] = 1

    return one_hot

def _action_seq2array(action_seq_list):
    action_seq_array = np.zeros((len(action_seq_list), 52), np.int8)
    for row, cards in enumerate(action_seq_list):
        action_seq_array[row, :] = _cards2array(cards)
    action_seq_array = action_seq_array.flatten()
    return action_seq_array

def _process_action_seq(sequence, length=9):
    sequence = [action[1] for action in sequence[-length:]]
    if len(sequence) < length:
        empty_sequence = ['' for _ in range(length - len(sequence))]
        empty_sequence.extend(sequence)
        sequence = empty_sequence
    return sequence
"""