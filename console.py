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

