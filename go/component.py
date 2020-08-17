from go import lib


class Board:
    def __init__(self, size):
        self.size = size
        self.matrix = []
        self.groups = set()

        for i in range(size):
            self.matrix.append([])
            for _ in range(size):
                self.matrix[i].append(Stone(-1))

    def place(self, stone, row, col):
        if self.matrix[row][col].color == -1:
            self.matrix[row][col] = stone
            return True, self.update_groups(stone, row, col) 
        return False, None


    def get_neighbours(self, row, col, stone=None):
        if stone is not None:
            for row in range(self.size):
                for col in range(self.size):
                    if stone == self.matrix[row][col]:
                        return self.get_neighbours(row=row, col=col)
            return None

        return [
            self.matrix[row][self.clamp(col - 1)],
            self.matrix[row][self.clamp(col + 1)],
            self.matrix[self.clamp(row - 1)][col],
            self.matrix[self.clamp(row + 1)][col],
        ]

    def update_groups(self, stone, row, col):
        similar_neighbours = []

        for neighbour in self.get_neighbours(row, col):
            if neighbour is None:
                continue
            if neighbour.color == stone.color and neighbour != stone:
                similar_neighbours.append(neighbour)
        return self.resolve_groups(stone, similar_neighbours)
        
    def resolve_groups(self, stone, neighbours):
        adjecent_groups = set()
        group = None

        for neighbour in neighbours:
            adjecent_groups.add(neighbour.group)

        if len(adjecent_groups) > 1:
            group = self.merge_groups(stone, neighbours, adjecent_groups)
        elif len(adjecent_groups) == 1:
            group = self.add_to_group(stone, neighbours, adjecent_groups.pop())
        else:
            group = self.create_new_group(stone, neighbours)
        return group

    def merge_groups(self, stone, neighbours, groups):
        merged_group = groups.pop()
        self.groups.remove(merged_group)

        while len(groups) != 0:
            group = groups.pop()
            merged_group = lib.Utils.merge(merged_group, group, stone, neighbours)
            self.groups.remove(group)

        for member_stone in merged_group:
            member_stone.group = merged_group

        self.groups.add(merged_group)
        return merged_group

    def add_to_group(self, stone, neighbours, group):
        group.add_vert_with_neighbours(stone, neighbours)
        stone.group = group
        return group

    def create_new_group(self, stone, neighbours):
        group = lib.Graph()
        group.add_vert_with_neighbours(stone, neighbours)

        self.groups.add(group)
        for neighbour in neighbours:
            neighbour.group = group

        stone.group = group
        return group

    def remove_group(self, group):
        if group is None:
            return
        self.groups.remove(group)

        for stone in group.get_vertices():
            stone.color = -1

    def remove_groups(self, groups):
        self.group = self.groups.difference(groups)

    def clamp(self, target_val, min_val=0, max_val=0):
        if max_val == 0:
            max_val = self.size - 1

        return max(min_val, min(target_val, max_val))

    def __hash__(self):
        string = ""

        for row in self.matrix:
            for element in row:
                string += str(element)

        return hash(string)

    def __str__(self):
        string = ""
        cell_size = 3

        borders = ["╔", "╗", "╚", "╝",
                   "║", "═", "┐", "┌",
                   "┘", "└", "├", "┤",
                   "┼", "─", "│", "┬",
                   "┴"]

        # Upper border
        string += borders[0] + ((self.size + 1) * (cell_size + 1) - 1) * borders[5] + borders[1] + "\n"

        # Horizontal lines and stones
        for row in range(self.size):
            string += borders[4] + cell_size * " "

            if row == 0:
                string += self.draw_row(row, cell_size, borders[7], borders[15], borders[6], borders[13])

            elif row < self.size - 1:
                string += self.draw_row(row, cell_size, borders[10], borders[12], borders[11], borders[13])
                    
            else:
                string += self.draw_row(row, cell_size, borders[9], borders[16], borders[8], borders[13])
                string += cell_size * " " + borders[4] + "\n"
                break

            string += cell_size * " " + borders[4] + "\n"
            string += borders[4] + self.size * (cell_size * " " + borders[14])
            string += cell_size * " " + borders[4]
            string += "\n"

        # Lower border
        string += borders[2] + ((self.size + 1) * (cell_size + 1) - 1) * borders[5] + borders[3] + '\n'

        return string

    def draw_row(self, row, cell_size, left_char, mid_char, right_char, filler_char):
        string = left_char if self.matrix[row][0].color == -1 else str(self.matrix[row][0])
        string += cell_size * filler_char

        for col in range(1, self.size - 1):
            string += mid_char if self.matrix[row][col].color == -1 else str(self.matrix[row][col])
            string += cell_size * filler_char
        string += right_char if self.matrix[row][self.size - 1].color == -1 else str(self.matrix[row][self.size - 1])

        return string


class Stone:
    def __init__(self, color):
        self.color = color
        self.group = None

    def __str__(self):
        return str(self.color)
