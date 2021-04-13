from random import choice

class Game_aux:
    
    def __init__(self, board, player1, player2):
        self.board = board
        self.players = [player1, player2]
        self.turn = 0
        self.on = True

    def check_win(self, board, currplayer):
        size=self.board.size
        if currplayer.color==1:
            for component in self.board.components[currplayer.color-1]:
                if self.board.north_component.issubset(component) and self.board.south_component.issubset(component):
                    return currplayer
        elif currplayer.color==2:
            for component in self.board.components[currplayer.color-1]:
                if self.board.west_component.issubset(component) and self.board.east_component.issubset(component):
                    return currplayer
        return None

    def run(self):
        while self.on:
            currplayer = self.players[self.turn]

            if currplayer.plays(self.board):
                self.turn = 1 - self.turn
            
            winner = self.check_win(self.board, currplayer)
            if winner != None:
                self.on = False
                return winner.color


class AI_player:

    def __init__(self, color):
        self.color = color

    def plays(self, board, i=None, j=None):
        if i == None:
            i, j = choice(board.actions)
        return board.update((i, j), self.color)


class Board:

    def __init__(self, board_size):
        self.size = int(board_size)
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
        self.actions = [(i,j) for i in range(self.size) for j in range(self.size)]
        self.east_component = set([(i,self.size) for i in range(self.size)])
        self.west_component = set([(i,-1) for i in range(self.size)])
        self.north_component = set([(-1,i) for i in range(self.size)])
        self.south_component = set([(self.size,i) for i in range(self.size)])
        self.components = [[self.north_component, self.south_component], [self.west_component, self.east_component]]


## Convert point and coord for display ##############################

    def coord_to_action(self, i, j):
        """ Convert board coord (i,j) to hexagon index in board actions. """
        return i * self.size + j

    def center_to_coord(self, tile_center):
        """ Convert tile_center to board coord (i,j). """
        index  = self.tiles_centers.index(tile_center)
        i = index // self.size
        j = index % self.size
        return i, j

###############################################################


## Fonction to create edge between tiles of the same color ########

    def get_neighbors(self, i, j):
        """ Returns the neighbours tiles of a tile (i,j) on the board. """
        neighbors = []
        for a in range(-1,2): 
            for b in range(-1,2):  
                if (a,b)!=(1,1) and (a,b)!=(0,0) and (a,b)!=(-1,-1):
                    neighbors.append((i+a,j+b))
        return neighbors

###############################################################


## Update board state after put a stone ######################

    def update(self, pos, color, center=False):
        """ Update the board after an action. """
        i, j = pos
        self.board[i][j] = color
        self.actions.remove((i,j))
        
        neighbors = self.get_neighbors(i,j)

        # adds tiles to other connected tiles
        added = False
        index = 0
        for component in self.components[color-1]:
            if component.intersection(neighbors) != set():
                self.components[color-1][index].add((i,j))
                added = True
            index += 1
        if not added:
            self.components[color-1].append(set([(i,j)]))
        #groups the adjacent components
        l = len(self.components[color-1])
        if l > 1:
            for index1 in range(l):
                for index2 in range(l):
                    if index1 != index2:
                        try:
                            if (i,j) in self.components[color-1][index1] and (i,j) in self.components[color-1][index2]:
                                self.components[color-1][index1] = self.components[color-1][index2] | self.components[color-1][index1]
                                self.components[color-1].remove(self.components[color-1][index2])                              
                        #in case we are considering an already deleted set
                        except IndexError:
                            pass
        return True

###############################################################


## Console display  ###########################################

    def __str__(self):
        """ Returns a string containing the current state of the board. """
        schema = ""
        headers = "     "
        alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        alphabet.reverse()

        red_line_top = headers + "\033[31m--\033[0m" * (len(self.board))

        i = 0
        for line in self.board:
            line_txt = ""
            headers += alphabet.pop() + " "

            line_txt += str(f" {i+1}")  + str(' ' * (i + 1))  + "\033[34m \\ \033[0m" if i < 9 \
                        else str(i + 1) + str(' ' * (i + 1)) + "\033[34m \\ \033[0m"

            for stone in line:
                if stone == 0:
                    line_txt += "⬡ "
                elif stone == 1:
                    line_txt +=  "\033[31m⬢ \033[0m" # 31=red
                else:
                    line_txt += "\033[34m⬢ \033[0m" # 34=blue

            schema += line_txt + "\033[34m \\ \033[0m" + "\n"

            i = i + 1

        red_line_bottom = (" " * (self.size)) + red_line_top

        return headers + "\n" + (red_line_top) + "\n" \
                + schema + red_line_bottom

##############################################################