#!/usr/bin/env python3
from AI.Hex_mc0 import *
from copy import deepcopy


'''def __deepcopy__(self, color):
    self.size = board.size
    self.board = board.board
    self.actions = board.actions
    self.currplayer = color
    self.east_component = board.east_component
    self.west_component = board.west_component
    self.north_component = board.north_component
    self.south_component = board.south_component
    self.components = board.components
    self.winner = None

    #the player running the mcts algorithm
    self.player = color
    return self'''

def mc0(initial_board, n, color, needDetails):

    # Final dict
    res = {action:0 for action in initial_board.actions}

    (RED, BLUE) = (1, 2) if color == 1 else (2,1)
    player1 = AI_player(RED)
    player2 = AI_player(BLUE)
    possible_plays = initial_board.actions

    #deepcopy doesn't work through pygame objects so elt's do it manually
    tboard = Board(initial_board.size)
    tboard.board = deepcopy(initial_board.board)
    tboard.actions = deepcopy(possible_plays)
    tboard.components = deepcopy(initial_board.components)
    
    #tboard = initial_board #deepcopy(initial_board)

    for action in possible_plays:
        games_won = 0

        for _ in range(n):
            tmp_board = deepcopy(tboard)
            tmp_game = Game_aux(tmp_board, player1, player2)
            i, j = action
            tmp_game.players[0].plays(tmp_game.board, i, j)
            winner = tmp_game.run()
            del tmp_game
            del tmp_board
            games_won += (winner == color)

        res[action] = games_won

    best_action = max(res, key = res.get)

    if needDetails :
        for action, score in res.items():
            if action != best_action:
                print(action,':',round(score/n,3))
            else:
                print("   ",action,':',round(score/n,3))
    
    return best_action

#####################################################