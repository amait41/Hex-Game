import sys
from time import time
import numpy as np
import matplotlib.pyplot as plt
from Board import Board
from Game import Game
from Player import AI



def test(testType, player1_type, player2_type, board_size):

    RED, BLUE = 1, 2
    ai_algorithms = ['random', 'mc', 'mc_ucb1', 'mcts']
    # init red player
    if player1_type in ai_algorithms:
        player1 = AI(RED, player1_type)
    else:
        raise Exception("Wrong player 1 type ")
    # init blue player
    if player2_type  in ai_algorithms:
        player2 = AI(BLUE, player2_type)
    else:
        raise Exception("Wrong player 2 type")
    # selects a test
    tests = {'test1': test1,
             'test2': test2}
    make_test = tests[sys.argv[5]]
    make_test(player1, player2, board_size, 10)


def test1(player1, player2, board_size, n=10):
    """find the """
    print('Simulations in progress...')
    time0 = time()
    RED, BLUE = 1, 2
    C = np.linspace(0,4,20)
    res = []

    if player2.algorithm.__name__ != 'mcts':
        raise Exception("Player 2 type must be mcts for test1.")

    for explorationConstant in C:
        print(explorationConstant)
        player2.explorationConstant = explorationConstant
        mcts_winrate = 0
        for i in range(n):
            print(i)
            board = Board(board_size)
            game = Game(board, player1, player2)
            mcts_winrate += game.runNoDisplay()

        res.append(mcts_winrate / n)
    print(f'Execution : {time()-time0}s')

    plt.scatter(C, res)
    plt.xlabel("Exploration constant", size = 16,)
    plt.ylabel("Winrate", size = 16)

    plt.title(f"UCT's winrate on {n} games vs {player1.algorithm.__name__}", 
          fontdict={'color' : 'darkblue',
                    'size': 14})

    plt.show()
    

def test2(player1, player2, board_size, n=10):
    print('Simulations in progress...')
    time0 = time()
    w = 0
    for i in range(n):
        board = Board(board_size)
        game = Game(board, player1, player2)
        w += game.runNoDisplay()    
    print(f'#games = {n}')
    print(f'Win rate Blue: {w/n}')
    t = time()-time0
    print(f'Time for {n} games: {round(t,3)}s')
    print(f'{round(n/t,3)} games/s')
    print(f'{round(n*60/t,3)} games/min')