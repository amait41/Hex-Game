import string
import numpy as np

class Board():

    def __init__(self, board_size):
        self.size = int(board_size)
        self.board = [[0 for i in range(self.size)] for j in range(self.size)] # np.zeros((self.size, self.size))

        self.east_component = set([(i,self.size) for i in range(self.size)])
        self.west_component = set([(i,-1) for i in range(self.size)])
        self.north_component = set([(-1,i) for i in range(self.size)])
        self.south_component = set([(self.size,i) for i in range(self.size)])

        #Connected components : [ [  compred1, ..., compredq  ],  [   compblue1, ..., compbluer  ]      ]  where comp...i is a list
        #red connected components : self.components[0],  blue connected components : self.components[1]
        self.components = [ [self.north_component, self.south_component], [self.west_component, self.east_component] ]

        self.actions = list(range(self.size**2))

    ## Convert point and coord for display ##########################
    def coord_to_action(self, i, j):
        """
        Convert board coord (i,j) to hexagon index in board.actions
        """
        return i * self.size + j


    def action_to_coord(self, action):
        """
        Convert hexagon index in board.actions to board coord (i,j).
        """
        return action // self.size, action % self.size
    ###############################################################


    ## Fonction to create edgse between tiles of the same color ########
    def get_neighbors(self, i, j):
        """
        Returns the neighbourhood of a point (i,j) of an hex matrix
        """
        b = np.array(self.board)
        neighbors=[]
        for a in range(-1,2): 
            for b in range(-1,2):  
                if (a,b)!=(1,1) and (a,b)!=(0,0) and (a,b)!=(-1,-1):
                    neighbors.append((i+a,j+b))
        return neighbors
    ###############################################################


    #### Update ############################################
    def update(self, color, i, j):

        self.board[i][j] = color
        action = self.coord_to_action(i,j)
        action_index = self.actions.index(action)
        self.actions.pop(action_index)

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
        length = len(self.components[color-1])
        if length>1:
            for index1 in range(length):
                for index2 in range(length):
                    if index1!=index2:
                        try:
                            #in case we are considering an already deleted list
                            if (i,j) in self.components[color-1][index1] and (i,j) in self.components[color-1][index2]:
                                self.components[color-1][index1] = self.components[color-1][index2] | self.components[color-1][index1]
                                self.components[color-1].remove(self.components[color-1][index2])
                        except IndexError:
                            pass

        return True
        ###############################################################

    ## Console display  ###########################################
    def __str__(self):
        """ This function returns a string containing the current state of the board """
        schema = ""
        headers = "     "
        alphabet = list(string.ascii_uppercase) 
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
