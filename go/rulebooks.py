class Empty:

    @staticmethod
    def check_board(board):
        return 0

    @staticmethod
    def count_points():
        return 0

class Standard(Empty):

    @staticmethod
    def check_current_move(board, group):
        captured_groups = Standard.check_board(board)

        # Check if move is legal
        if len(captured_groups) == 1 and group == captured_groups[0]:
            return False, captured_groups
        return True, captured_groups

    @staticmethod
    def check_board(board):
        captured_groups = []

        for group in board.groups:
            captured = Standard.check_group(board, group)
            if captured:
                captured_groups.append(group)

        return captured_groups

    @staticmethod
    def check_group(board, group):
        for stone in group.get_vertices_with_less_than_n_neighbours(4):
            for neighbour in board.get_neighbours(0, 0, stone=stone):
                if neighbour.color == -1: 
                    return False
        return True

    @staticmethod
    def count_scores(players):
        scores = [0] * len(players)

        for index, player in enumerate(players):
            for stone in player.stones:
                if stone.color == -1:
                    scores[index] -= 1
            scores[index] += len(player.stones)

        return scores
