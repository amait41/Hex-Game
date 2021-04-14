import random
from math import sqrt
from AI.Hex import Hex
from AI.mc import MC
from AI.mc_ucb1 import MC_UCB1
from AI.mcts import MCTS
from copy import deepcopy
from time import time

n = 100

def rand(board, color, explorationConstant=None):
    """
    Pick a random legal action.
    """
    return random.choice(board.actions)

def mc(board, color, explorationConstant=None):
    """
    Plays games with iteration or time limit.
    The same number of games is played for each action.
    Random policy is use.
    Return the action with the best win rate.
    """
    initialState = Hex(color, deepcopy(board))
    searcher = mc(timeLimit=None, iterationLimit=n)
    action = searcher.search(initialState=initialState, needDetails=False)
    return action

def mc_ucb1(board, color, explorationConstant=sqrt(2)):
    """
    Plays games with iteration or time limit.
    The actions are selected with UCB1 criterion.
    Random policy is use.
    Return the action with the best win rate.
    """
    initialState = Hex(color, board)
    searcher = mc_ucb1(timeLimit=None, iterationLimit=n, explorationConstant=explorationConstant)
    action = searcher.search(initialState=initialState, needDetails=False)
    return action

def mcts(board, color, explorationConstant=sqrt(2)):
    """
    Uses mcts method with time (ms) or iteration limit.
    """
    initialState = Hex(color, deepcopy(board))
    searcher = MCTS(timeLimit=None, iterationLimit=n, explorationConstant=explorationConstant)
    action = searcher.search(initialState=initialState, needDetails=False)
    return action