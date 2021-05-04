from misc import display
if display:
    import pygame
    from misc import screen

class Game:
    
    def __init__(self, board, player1, player2):
        self.board = board
        self.players = [player1, player2]
        self.turn = 0
        # changer self.on en self.winner
        self.on = True

    def check_win(self, currplayer):
        """
        Checks if a the current player won the game. 
        Returns the winner's name if there is any or None if there is none.
        1 : red player
        2 : blue player
        """
        for component in self.board.components[currplayer.color - 1]:
            if currplayer.color == 1:
                if self.board.north_component.issubset(component) \
                    and self.board.south_component.issubset(component):
                    return currplayer
            else: # currplayer.color == 2
                if self.board.west_component.issubset(component) \
                    and self.board.east_component.issubset(component):
                    return currplayer
        return None
    

    def run(self):

        pause = True
        
        while self.on:
            
            for event in pygame.event.get():
                pygame.display.flip()
                currplayer = self.players[self.turn]

                # upon pressing QUIT button
                if event.type == pygame.QUIT: 
                    self.on = False
                
                # ESC button
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.on = False
                
                # when current human player plays
                elif currplayer.__class__.__name__ == 'Human':
                    if event.type == pygame.MOUSEBUTTONDOWN and \
                        pygame.mouse.get_pressed(num_buttons=3)==(True,False,False):
                        if currplayer.plays(self.board):
                            self.turn = 1 - self.turn
                            #print(self.board)
                
                # current computer player plays
                elif currplayer.__class__.__name__ == 'AI':
                    if currplayer.plays(self.board):
                        self.turn = 1 - self.turn
                        #print(self.board)

                # did someone win ?
                winner = self.check_win(currplayer)
                if winner != None:
                    self.on = False
                    print(f"It's over! {winner.name} won!")
                    # pick a font and writes the winner
                    font = pygame.font.SysFont("Times New Roman", 30)
                    label = font.render(f"  {winner.name} won!", 1, (255, 255, 255))
                    screen.blit(label, (0, 0))
                    pygame.display.flip()
                    break

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.on = False
                    pause=False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.on = False
                        pause=False


    def runNoDisplay(self):
        while self.on:
            currplayer = self.players[self.turn] 
            if currplayer.plays(self.board):
                self.turn = 1 - self.turn

            # did someone win ?
            winner = self.check_win(currplayer)
            if winner != None:
                return int(winner.color) - 1
