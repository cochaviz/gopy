import os

from go import component
from go import rulebooks

class Player:
    def __init__(self, color):
        self.color = color
        self.stones = []

    def place(self, row, col, board):
        placed_stone = component.Stone(self.color)
        valid, placed_group = board.place(placed_stone, row, col)

        if valid:
            self.stones.append(placed_stone)
            return True, placed_group
        return False, placed_group

    def get_input(self):
        position = input("Player " + str(self.color) + " enter a position to place the stone at [row, column]: ")
        try:
            position = list(map(int, position.split(", ")))
            assert len(position) == 2
        except:
            print("Please enter properly formatted value of the form: row, column")
            return self.get_input()

        return position[0], position[1]


class Game:
    def __init__(self, board=None, size=13, rulebook=rulebooks.Empty(), number_of_players=2):
        if board is None:
            self.board = component.Board(size)
        self.players = []

        for i in range(number_of_players):
            self.players.append(Player(i))

        self.rulebook = rulebook
        self.states = set()

    def start(self):
        try:
            while True:
                for player in self.players:
                    # TEMPORARY
                    self.clear()
                    print(self.board)
                    # TEMPORARY 

                    self.states.add(hash(self.board))  
                    group = self.make_move(player)

                    while not self.check_board(group):
                        print("Please, make a legal move!")
                        group = self.make_move(player)

        except KeyboardInterrupt:
            self.clear()
            print(self.board)
            self.end_game()

    def make_move(self, player):
        row, col = player.get_input()

        try:
            valid, group = player.place(row, col, self.board)
            if not valid:
                print("Please put your stone in a an empty place!")
                return self.make_move(player)
        except IndexError:
            print("Please put your stone inside the board!")
            return self.make_move(player)
        return group
        
    def check_board(self, group):
        valid, captured_groups = self.rulebook.check_current_move(self.states, self.board, group)
        
        for group in captured_groups:
            self.board.remove_group(group)

        return valid

    def end_game(self):
        scores = self.rulebook.count_scores(self.players)
        print("Player " + str(scores.index(max(scores))) + " won!")

        for index, score in enumerate(scores):
            print("Player " + str(index) + " scored " + str(score) + " points")


    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
