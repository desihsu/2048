import random
import time
import displayer
import players


class GameManager:
    def __init__(self, size=4):
        self.grid = displayer.Grid(size)
        self.computerAI = players.ComputerAI()
        self.playerAI = players.PlayerAI()
        self.possible_new_tiles = (2, 4)
        self.probability = 0.9
        self.time_limit = 0.25
        self.over = False

    def check_timer(self, current_time):
        if current_time - self.prev_time > self.time_limit:
            self.over = True
        else:
            while time.clock() - self.prev_time < self.time_limit: pass
            self.prev_time = time.clock()

    def start(self):
        actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        PLAYER_TURN, COMPUTER_TURN = 0, 1
        max_tile = 0

        for i in range(2):
            self.insert_random_tile()
        self.grid.display()

        turn = PLAYER_TURN
        self.prev_time = time.clock()

        while self.grid.can_move() and not self.over:
            grid_copy = self.grid.clone()
            move = None

            if turn == PLAYER_TURN:
                print("Player's Turn:", end="")
                move = self.playerAI.get_move(grid_copy)
                print(actions[move])
                self.grid.move(move)
                max_tile = self.grid.get_max_tile()
            else:
                print("Computer's Turn:")
                move = self.computerAI.get_move(grid_copy)
                self.grid.insert_tile(move, self.get_new_tile_value())

            self.grid.display()
            self.check_timer(time.clock())
            turn = 1 - turn

        print(max_tile)

    def get_new_tile_value(self):
        if random.randint(0, 99) < 100 * self.probability:
            return self.possible_new_tiles[0]
        else:
            return self.possible_new_tiles[1]

    def insert_random_tile(self):
        tile_value = self.get_new_tile_value()
        cells = self.grid.get_available_cells()
        cell = cells[random.randint(0, len(cells)-1)]
        self.grid.insert_tile(cell, tile_value)


if __name__ == "__main__":
    game = GameManager()
    game.start()