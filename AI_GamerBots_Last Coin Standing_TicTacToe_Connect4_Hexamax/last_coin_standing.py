from easyAI import TwoPlayersGame, id_solve, Human_Player, AI_Player
from easyAI.AI import TT

class LastCoinStanding(TwoPlayersGame):
    def __init__(self, players):
        # Defining the players. Necessary parameter.
        self.player = players

        # Defining who starts the game. Necessary parameter.
        self.nplayer = 1 

        # Overall number of coins in the pile 
        self.num_coin = 25

        # Defining max number of coins per move 
        self.max_coin = 4 

    # Defining possible moves
    def possible_move(self): 
        return [str(x) for x in range(1, self.max_coin + 1)]
    
    # Removing coins
    def make_move(self, move): 
        self.num_coin -= int(move) 

    # Checking if the opponent took out the last coin?
    def win(self): 
        return self.num_coin <= 0 

    # Stopping the game when somebody wins 
    def if_over(self): 
        return self.win() 

    # Computing score
    def scoring(self): 
        return 100 if self.win() else 0

    # Showing number of coins remaining in the pile
    def show(self): 
        print(self.num_coin, 'coins left in the pile')

if __name__ == "__main__":
    # Defining the transposition table
    tt = TT()

    LastCoinStanding.ttentry = lambda self: self.num_coins

    result, depth, move = id_solve(LastCoinStanding, 
            range(2, 20), win_score=100, tt=tt)
    print(result, depth, move)  

    game = LastCoinStanding([AI_Player(tt), Human_Player()])
    game.play() 

