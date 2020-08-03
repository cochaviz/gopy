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

        if len(captured_groups) == 1 and group in captured_groups:
            return False, captured_groups
        return True, captured_groups
    
    @staticmethod
    def check_board(board):
        captured_groups = []

        for group in board.groups:
            captured_groups.append(Standard.check_group(board, group))
        return captured_groups

    @staticmethod
    def check_group(board, group):
        for stone in group.get_vertices_with_less_than_n_neighbours(4):
            for neighbour in board.get_neighbours(0, 0, stone=stone):
                if neighbour.color == -1: 
                    return None
        return group
    