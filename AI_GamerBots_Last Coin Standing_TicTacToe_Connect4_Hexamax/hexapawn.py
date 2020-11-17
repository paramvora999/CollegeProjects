
from easyAI import TwoPlayersGame, AI_Player, \
        Human_Player, Negamax

class GameControl(TwoPlayersGame):
    def __init__(self, players, size = (4, 4)):
        self.size = size
        num_pawn, len_board = size
        p = [[(i, j) for j in range(len_board)] \
                for i in [0, num_pawn - 1]]

        for i, d, goal, pawn in [(0, 1, num_pawn - 1, 
                p[0]), (1, -1, 0, p[1])]:
            player[i].direction = d
            player[i].goal_line = goal
            player[i].pawn = pawn

        self.player = player

        self.nplayer = 1

        self.alphabet = 'ABCDEFGHIJ'

        self.to_tuple = lambda s: (self.alphabet.index(s[0]), 
                int(s[1:]) - 1)

        self.to_string = lambda move: ' '.join([self.alphabet[
                move[i][0]] + str(move[i][1] + 1)
                for i in (0, 1)])

    # Defining the possible moves
    def possible_move(self):
        move = []
        opponent_pawn = self.opponent.pawn
        d = self.player.direction

        for i, j in self.player.pawn:
            if (i + d, j) not in opponent_pawn:
                move.append(((i, j), (i + d, j)))

            if (i + d, j + 1) in opponent_pawn:
                move.append(((i, j), (i + d, j + 1)))

            if (i + d, j - 1) in opponent_pawn:
                move.append(((i, j), (i + d, j - 1)))

        return list(map(self.to_string, [(i, j) for i, j in move]))

    # Defining how to make a move
    def make_move(self, move):
        move = list(map(self.to_tuple, move.split(' ')))
        ind = self.player.pawn.index(move[0])
        self.player.pawn[ind] = move[1]

        if move[1] in self.opponent.pawn:
            self.opponent.pawn.remove(move[1])

    # Defining what a loss looks like
    def loss_condition(self):
        return (any([i == self.opponent.goal_line
                for i, j in self.opponent.pawn])
                or (self.possible_moves() == []) )

    def if_over(self):
        return self.loss_condition()

    # Show the current status
    def show_status(self):
        f = lambda x: '1' if x in self.player[0].pawn else (
                '2' if x in self.player[1].pawn else '.')

        print("\n".join([" ".join([f((i, j))
                for j in range(self.size[1])])
                for i in range(self.size[0])]))

if __name__=='__main__':
    # Compute the score
    scoring = lambda game: -100 if game.loss_condition() else 0

    # Define the algorithm
    algorithm = Negamax(12, scoring)

    # Start the game
    game = GameControl([AI_Player(algorithm), 
            AI_Player(algorithm)])
    game.play()
    print('\nPlayer', game.nopponent, 'wins after', game.nmove , 'turns')

