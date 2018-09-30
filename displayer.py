import copy


class Grid:
    def __init__(self, size=4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]
        self.dir_vecs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.vec_index = range(4)

    def display(self):
        for i in range(self.size):
            for j in range(self.size):
                print("%6d  " % self.map[i][j], end="")
            print("")
        print("")

    def clone(self):
        grid_copy = Grid()
        grid_copy.map = copy.deepcopy(self.map)
        grid_copy.size = self.size
        return grid_copy

    def insert_tile(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    def get_available_cells(self):
        cells = []

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    cells.append((x, y))

        return cells

    def get_max_tile(self):
        max_tile = 0

        for x in range(self.size):
            for y in range(self.size):
                max_tile = max(max_tile, self.map[x][y])

        return max_tile

    def move(self, dir):
        UP, DOWN, LEFT, RIGHT = range(4)
        dir = int(dir)

        if dir == UP:
            return self.moveUD(False)
        if dir == DOWN:
            return self.moveUD(True)
        if dir == LEFT:
            return self.moveLR(False)
        if dir == RIGHT:
            return self.moveLR(True)

    def moveUD(self, down):
        r = range(self.size-1, -1, -1) if down else range(self.size)
        moved = False

        for j in range(self.size):
            cells = []
            for i in r:
                cell = self.map[i][j]
                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for i in r:
                value = cells.pop(0) if cells else 0
                if self.map[i][j] != value:
                    moved = True
                self.map[i][j] = value

        return moved

    def moveLR(self, right):
        r = range(self.size-1, -1, -1) if right else range(self.size)
        moved = False

        for i in range(self.size):
            cells = []
            for j in r:
                cell = self.map[i][j]
                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for j in r:
                value = cells.pop(0) if cells else 0
                if self.map[i][j] != value:
                    moved = True
                self.map[i][j] = value

        return moved

    def merge(self, cells):
        if len(cells) <= 1:
            return cells
        i = 0

        while i < len(cells) - 1:
            if cells[i] == cells[i+1]:
                cells[i] *= 2
                del cells[i+1]
            i += 1

    def can_move(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y]:
                    for i in self.vec_index:
                        move = self.dir_vecs[i]
                        adj_cell_value = self.get_cell_value((x + move[0], 
                                                              y + move[1]))
                        if (adj_cell_value == self.map[x][y] or 
                            adj_cell_value == 0):
                            return True
                elif self.map[x][y] == 0:
                    return True
        return False

    def get_available_moves(self):
        available_moves = []

        for x in self.vec_index:
            grid_copy = self.clone()
            if grid_copy.move(x):
                available_moves.append(x)

        return available_moves

    def get_cell_value(self, pos):
        crossbound = (pos[0] < 0 or pos[0] >= self.size or
                      pos[1] < 0 or pos[1] >= self.size)
        if not crossbound:
            return self.map[pos[0]][pos[1]]
        else:
            return None