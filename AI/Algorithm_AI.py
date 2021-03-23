from random import choice
from AI.mc.best_action import best_action

#from AI.mcts.Game_mc import *
#from AI.mcts.mc import *

from AI.mcts.Game_mcts import *
from AI.mcts.mcts import *

from copy import deepcopy

def run_random(board, color):
    """
    Pick a random legal action.
    """
    return board.action_to_coord(choice(board.actions))


def run_mc(board, color):
    """
    Plays n games with random policy for each legal actions.
    Return the action with the best win rate.
    """
    """
    initialState = Hex(color, deepcopy(board))
    searcher = mc(iterationLimit=1000)
    action = searcher.search(initialState=initialState)
    return (action.x, action.y)
    """
    n = 10
    action = best_action(board, n, color)
    return board.action_to_coord(action)


def run_mcts(board, color):
    """
    Uses mcts method with time (ms) or iteration limit.
    """
    initialState = Hex(color, deepcopy(board))
    searcher = mcts(iterationLimit=100)
    action = searcher.search(initialState=initialState, needDetails=False)
    return (action.x, action.y)