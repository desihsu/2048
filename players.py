import itertools
import math
import random
import time


class ComputerAI:
    def get_move(self, grid):
        cells = grid.get_available_cells()
        return cells[random.randint(0, len(cells)-1)]


class PlayerAI:
    def get_move(self, grid):
        max_utility = -math.inf
        best_move = None

        for move in grid.get_available_moves():
            grid_clone = grid.clone()
            grid_clone.move(move)
            utility = self.minimize(grid_clone, -math.inf, math.inf, 
                                    time.clock(), 0)
            if utility >= max_utility:
                max_utility = utility
                best_move = move

        return best_move

    def get_children(self, grid, maximizing=True):
        children = []

        if maximizing:
            for move in grid.get_available_moves():
                child = grid.clone()
                child.move(move)
                children.append(child)
        else:
            for cell in grid.get_available_cells():
                for i in (2, 4):
                    child = grid.clone()
                    child.insert_tile(cell, i)
                    children.append(child)

        return children

    def minimize(self, grid, alpha, beta, start, depth):
        if not grid.can_move() or depth == 4 or (time.clock() - start) > 0.04:
            return self.evaluate(grid)
        min_utility = math.inf
        
        for child in self.get_children(grid, maximizing=False):
            utility = self.maximize(child, alpha, beta, start, depth+1)

            if utility < min_utility:
                min_utility = utility
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility

        return min_utility

    def maximize(self, grid, alpha, beta, start, depth):
        if not grid.can_move() or depth == 4 or (time.clock() - start) > 0.04:
            return self.evaluate(grid)
        max_utility = -math.inf

        for child in self.get_children(grid):
            utility = self.minimize(child, alpha, beta, start, depth+1)
            
            if utility > max_utility:
                max_utility = utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility

        return max_utility

    def evaluate(self, grid):
        if not grid.can_move():
            return -math.inf

        corners = [0, 0, 0, 0]
        bottom_right = [[j for j in range(i, i+4)] for i in range(-3, 1)]
        top_right = bottom_right[::-1]
        top_left = [i[::-1] for i in top_right]
        bottom_left = top_left[::-1]
    
        for x in range(4):
            for y in range(4):
                corners[0] += bottom_right[x][y] * grid.map[x][y]
                corners[1] += top_right[x][y] * grid.map[x][y]
                corners[2] += top_left[x][y] * grid.map[x][y]
                corners[3] += bottom_left[x][y] * grid.map[x][y]
  
        return max(corners)