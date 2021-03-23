import string

class Board:

    def __init__(self, board_size, background, screen):
        self.size = int(board_size)
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
        self.actions = list(range(self.size**2))

        # init connex componant list
        self.east_component = set([(i,self.size) for i in range(self.size)])
        self.west_component = set([(i,-1) for i in range(self.size)])
        self.north_component = set([(-1,i) for i in range(self.size)])
        self.south_component = set([(self.size,i) for i in range(self.size)])
        #Connected components : [[comp_red_1, ..., comp_red_n], [comp_blue_1, ..., comp_blue_n]]  where comp_color_i is a list
        #red connected components : self.components[0],  blue connected components : self.components[1]
        self.components = [[self.north_component, self.south_component], [self.west_component, self.east_component]]

        #create landmark and get tiles' center
        (x0,y0)=(106,128)
        y0-=20 #initial shift
        x0-=67
        self.tiles_centers = []
        for i in range(1, self.size+1):
            y0 = y0 + 57.7
            x0 +=  33.6
            for j in range(1, self.size+1):
                point = (x0+j*66.7, y0)
                # add hexagon center
                self.tiles_centers.append(point)


## Convert point and coord for display ##############################

    def coord_to_action(self, i, j):
        """ Convert board coord (i,j) to hexagon index in board actions. """
        return i * self.size + j


    def action_to_coord(self, action):
        """ Convert hexagon index in board.actions to board coord (i,j). """
        return action // self.size, action % self.size


    def center_to_coord(self, tile_center):
        """ Convert tile_center to board coord (i,j). """
        index  = self.tiles_centers.index(tile_center)
        i = index // self.size
        j = index % self.size
        return i, j


    def get_polygon(self, pos, center=False):
        """
        Retourne la liste des poss déterminant l'hexagone contenant le pos entré en argument
        L'argument center indique si le pos entré est le pos central de l'hexagone, auquel cas on a pas besoin
        de faire tout un calcul fastidieux
        """

        #Paramètres globaux déterminant la taille des hexagones joués
        l = 64
        h = 74.3

        if center:
            x, y = pos[0], pos[1]
            hex_vertices = [(x+l/2,y-h/4), (x+l/2,y+h/4), (x,y+h/2), (x-l/2,y+h/4), (x-l/2,y-h/4), (x,y-h/2)]
            return hex_vertices, pos

        min_pos = self.tiles_centers[0]
        k = 0

        while True:
            try:
                p = self.tiles_centers[k]
                diff1 = (p[0]-pos[0], p[1]-pos[1])
                diff2 = (min_pos[0]-pos[0], min_pos[1]-pos[1])
                norm_diff1 = (diff1[0]**2+diff1[1]**2)**(1/2)
                norm_diff2 = (diff2[0]**2+diff2[1]**2)**(1/2)
                if norm_diff1 < norm_diff2:
                    min_pos = self.tiles_centers[k]
            except IndexError:
                break
            k += 1
        
        x, y = min_pos
        hex_vertices = [(x+l/2,y-h/4),(x+l/2,y+h/4),(x,y+h/2),(x-l/2,y+h/4),(x-l/2,y-h/4),(x,y-h/2)]
        return hex_vertices, min_pos

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

        # gets the center and the vertices' hex where the current player is willing to play
        hex_vertices, tile_center = self.get_polygon(pos,center)
        i, j = self.center_to_coord(tile_center)
        
        if self.board[i][j] == 0:
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
            return hex_vertices
        
        else:
            return None

###############################################################


## Console display  ###########################################

    def __str__(self):
        """ Returns a string containing the current state of the board. """
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
