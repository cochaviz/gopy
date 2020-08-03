import os

from go import component
from go import rulebooks


class Player:
    def __init__(self, color):
        self.color = color
        self.captured_stones = 0

    def place(self, row, col, board):
        return board.place(component.Stone(self.color), row, col)

    def get_input(self):
        position = input("Player " + str(self.color) + " enter a position to place the stone at [row, column]: ")
        position = list(map(int, position.split(", ")))

        return position[0], position[1]


class Game:
    def __init__(self, board=None, size=13, rulebook=rulebooks.Empty(), number_of_players=2):
        if board is None:
            self.board = component.Board(size)
        self.players = []

        for i in range(number_of_players):
            self.players.append(Player(i))

        self.rulebook = rulebook

    def start(self):
        while True:
            for player in self.players:
                self.clear()

                print(self.board)
                group = self.make_move(player)

                while not self.check_board(group):
                    print("Please make a legal move!")
                    group = self.make_move(player)

    def make_move(self, player):
        row, col = player.get_input()
        valid, group = player.place(row, col, self.board)

        try:
            if not valid:
                print("Please put your stone in a an empty place!")
                self.make_move(player)
        except IndexError:
            print("Please put your stone inside the board!")
            self.make_move(player)
        return group
        
    def check_board(self, group):
        valid, captured_groups = self.rulebook.check_current_move(self.board, group)
        
        for group in captured_groups:
            self.board.remove_group(group)

        return valid

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
