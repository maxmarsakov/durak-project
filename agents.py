"""
all the agents
"""

class Agent:
    pass

class HumanAgent(Agent):

    def __init__(self, playerName, playerNum=0):
        self.playerNum = playerNum
        self.playerName = playerName

class SimpleAgent(Agent):

    def __init__(self, playerName, playerNum=0):
        self.playerNum = playerNum
        self.playerName = playerName

class RandomAgent(Agent):

    def __init__(self, playerName, playerNum=0):
        self.playerNum = playerNum
        self.playerName = playerName

class MinimaxAgent(Agent):

    def __init__(self, playerName, playerNum=0):
        self.playerNum = playerNum
        self.playerName = playerName

class ReflexAgent(Agent):

    def __init__(self, playerName, playerNum=0):
        self.playerNum = playerNum
        self.playerName = playerName