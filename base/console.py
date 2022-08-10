from colorama import init

lastIndexBreak = False
init()

# design
SUIT_ICONS = {
    "-1": 'Stop', "C":'♣', "H":'♥' ,"D":'♦' ,"S":'♠'
}

def print_(text, end = '\n', startWith = '', endWith = ''):
    global lastIndexBreak
    
    if(lastIndexBreak):
        startWith = ''
        lastIndexBreak = False

    if(endWith == '\n'):
        lastIndexBreak = True
    
    lastText = startWith + text + endWith
    print (lastText, end = str(end) + "\n")

def format_suit_card(suitString, text=""):
    formattedSuit = SUIT_ICONS[suitString]

    if(suitString in ['H','D']): 
        color = '\033[91m'   
    else: 
        color = '\033[30m'
    return f'\033[47m {color}{formattedSuit}\033[00m\033[47m\033[30m {text} \033[00m' 

def __format_table( table):
    # helper function to represent the table graphically
    table_cards = list(reversed(table.cards))
    n = len(table_cards)
    formatted_table = ""
    for i in range(0,n,2):
        formatted_table += repr(table_cards[i])
        if (i < n-1): 
            formatted_table += " -> " + repr(table_cards[i+1])
        formatted_table += "\n"
    return formatted_table

def print_round_info(game):
    # helper function to represent the table graphically
    print_('The table: \n ', __format_table(game.table) )

