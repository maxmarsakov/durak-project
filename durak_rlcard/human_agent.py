from rlcard.utils.utils import print_card
from durak2 import Card

class HumanAgent(object):
    ''' A human agent for Blackjack. It can be used to play alone for understand how the blackjack code runs
    '''

    def __init__(self, num_actions):
        ''' Initilize the human agent

        Args:
            num_actions (int): the size of the output action space
        '''
        self.use_raw = True
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        _print_state(state['raw_obs'], state['raw_legal_actions'], state['action_record'])

        role = 'attacker' if state['raw_obs']['isAttacker'] else 'defender'
        current_player = state['raw_obs']['current_player']
        action = int(input(f'>> Player {current_player},{role}. You choose action (integer): '))

        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['raw_legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        return self.step(state), {}

def __format_table( table):
    # helper function to represent the table graphically
    table_cards = list(reversed(table.cards))
    n = len(table_cards)
    formatted_table = "=====table====\n"
    for i in range(0,n,2):
        formatted_table += repr(table_cards[i])
        if (i < n-1): 
            formatted_table += " -> " + repr(table_cards[i+1])
        formatted_table += "\n"
    formatted_table += "=============\n"
    return formatted_table

# design
SUIT_ICONS = {
    "-1": 'Stop', "C":'♣', "H":'♥' ,"D":'♦' ,"S":'♠'
}
def _format_suit_card(suitString, text=""):
    formattedSuit = SUIT_ICONS[suitString]

    if(suitString in ['H','D']): 
        color = '\033[91m'   
    else: 
        color = '\033[30m'
    return f'\033[47m {color}{formattedSuit}\033[00m\033[47m\033[30m {text} \033[00m' 


def _print_state(state, raw_legal_actions, action_record):
    ''' Print out the state

    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the each player's historical actions
    '''
    _action_list = []
    for i in range(1, len(action_record)+1):
        _action_list.insert(0, action_record[-i])
    #for pair in _action_list:
    #    print('>> Player', pair[0], 'chooses', pair[1])
    
    print("deck size", state['deckSize'])
    print("opponentHandSize", state['opponentHandSize'])
    print("current trump is", _format_suit_card(Card.SUITS[state['trumpSuit']]))
    print(__format_table(state['table']))
    print("your hand", state['hand'])
    print("legal actions", raw_legal_actions)

    """
    print('\n=============   Dealer Hand   ===============')
    print_card(state['dealer hand'])

    num_players = 2

    for i in range(num_players):
        print('===============   Player {} Hand   ==============='.format(i))
        print_card(state['player' + str(i) + ' hand'])

    print('\n=========== Actions You Can Choose ===========')
    print(', '.join([str(index) + ': ' + action for index, action in enumerate(raw_legal_actions)]))
    print('')
    """
