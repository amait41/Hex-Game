import numpy as np
import matplotlib.pyplot as plt
from Board import Board
from Game import Game
from Player import Human, AI



def test(testType,player1Type,player2Type,board_size):
    ai_algorithms = ['random', 'mc0', 'mc', 'mc_ucb1', 'mcts']

    if player1Type not in ai_algorithms:
        raise Exception("Wrong player 1 type ")
    if player2Type not in ai_algorithms:
        raise Exception("Wrong player 2 type")
    
    if testType == 'test1':
        #mcts vs another algo
        test1(player1Type,player2Type,board_size)

    elif testType == 'test2':
        pass


def test1(player1Type,player2Type,board_size,n=100):

    C = np.linspace(0,2,10)
    res = []
    RED, BLUE = 1, 2

    if player1Type not in ['mc_ucb1','mcts']:
        player1 = AI(RED, player1Type)
    elif player2Type not in ['mc_ucb1','mcts']:
        player2 = AI(RED, player1Type)
    else:
        raise Exception("run test2 to compare two mcts")

    for explorationConstant in C:
        print(explorationConstant)

        if player1Type in ['mc_ucb1','mcts']:
            player1 = AI(BLUE, player1Type, explorationConstant)
        elif player2Type in ['mc_ucb1','mcts']:
            player2 = AI(BLUE, player2Type, explorationConstant)
        blueWinrate = 0

        for i in range(n):
            board = Board(board_size)
            game = Game(board, player1, player2)
            blueWinrate += game.runNoDisplay()

        res.append(blueWinrate/n)

    plt.plot(C,res)
    plt.xlabel("Exploration constant", size = 16,)
    plt.ylabel("Winrate", size = 16)

    plt.title(f"Winrate of mcts for {n} games", 
          fontdict={'family': 'serif', 
                    'color' : 'darkblue',
                    'weight': 'bold',
                    'size': 18})

    plt.show()

def test2():
    pass