from random import choice
from copy import deepcopy
from time import time
from math import sqrt

from AI.Hex import Hex
from AI.mc import MC
from AI.mc_ucb1 import MC_UCB1
from AI.uct import UCT

n = 10000

def random(board, color, explorationConstant):
    """
    Pick a random legal action.
    """
    return choice(board.actions)


def mc(board, color, explorationConstant):
    """
    Plays games with iteration or time limit.
    The same number of games is played for each action.
    Random policy is use.
    Return the action with the best win rate.
    """
    initialState = Hex(color, deepcopy(board))
    searcher = MC(timeLimit=None, iterationLimit=n)
    action = searcher.search(initialState=initialState, needDetails=True)
    return action


def mc_ucb1(board, color, explorationConstant):
    """
    Plays games with iteration or time limit.
    The actions are selected with UCB1 criterion.
    Random policy is use.
    Return the action with the best win rate.
    """
    initialState = Hex(color, board)
    searcher = MC_UCB1(explorationConstant, timeLimit=None, iterationLimit=n)
    action = searcher.search(initialState=initialState, needDetails=True)
    return action


def uct(board, color, explorationConstant):
    """
    Plays games with iteration or time limit.
    Uses UCT method and UCB1 criterion for node selection.
    Random policy is use.
    Return the action with the best win rate.
    """
    initialState = Hex(color, deepcopy(board))
    searcher = UCT(explorationConstant, timeLimit=None, iterationLimit=n)
    tree, action = searcher.search(initialState=initialState, needDetails=True)
    return action


def uct_wm(board, color, explorationConstant, tree):
    """
    Plays games with iteration or time limit.
    Uses UCT method and UCB1 criterion for node selection.
    Reuse information from the previously created tree.
    Random policy is use.
    Return the action with the best win rate.
    """
    initialState = Hex(color, deepcopy(board))
    searcher = UCT(explorationConstant, timeLimit=None, iterationLimit=n)
    new_tree = cut(tree, initialState)
    tree, action = searcher.search(initialState=initialState, needDetails=True, root=new_tree)
    return tree, action


def cut(root, initialState):
    try:
        for child in root.children.values():
            if child.state.board == initialState.board:
                child.parent = None
                return deepcopy(child)
    except AttributeError:
        return None
