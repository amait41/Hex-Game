class Game:
    
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
