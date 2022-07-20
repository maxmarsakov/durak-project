from colorama import init

lastIndexBreak = False
init()

def print_(text, end = '\n', startWith = '', endWith = ''):
    global lastIndexBreak
    
    if(lastIndexBreak):
        startWith = ''
        lastIndexBreak = False

    if(endWith == '\n'):
        lastIndexBreak = True
    
    lastText = startWith + text + endWith
    print (lastText, end = end)

