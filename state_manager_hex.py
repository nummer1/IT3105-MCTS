import copy


class state_manager_hex:
    def __init__(self, size, start_player):
        self.size = size
        self.start_player = start_player
        # player 1 should always move first, start_player should be 1
        if self.start_player != 1:
            print("WARNING: start_player is not 1")

    def print_board(self, state_key):
        print("player_turn:", state_key[0])
        modcol = self.size - 1
        size = 2 * self.size - 1
        diamond_grid = [['*' for i in range(size)] for j in range(size)]
        for i, cell in enumerate(state_key[1]):
            c_column = i % self.size
            c_row = i // self.size
            newrow = c_row + c_column
            newcol = modcol + c_column - c_row
            if cell[0] == 1:
                value = 1
            elif cell[1] == 1:
                value = 2
            else:
                value = 0
            diamond_grid[newrow][newcol] = str(value)
        for row in diamond_grid:
            print(' '.join(row))

    def get_start(self):
        # return start state
        # board = Board(self.size, self.start_player)
        board = [(0, 0) for i in range(self.size**2)]
        return (self.start_player, board)

    def get_child_state_keys(self, state_key):
        # must return a list of unique keys for all legal child states
        # returns state and moves made to get to the state
        legal_states = []
        legal_moves = []
        cur_player = state_key[0]
        next_player = 1 if cur_player == 2 else 2
        board = state_key[1]
        for i, cell in enumerate(board):
            if cell == (0, 0):
                # if the hex is empty
                # use copy. list is single dimension. tuples are copied correctly
                b = copy.copy(board)
                if cur_player == 1:
                    b[i] = (1, 0)
                else:
                    b[i] = (0, 1)
                legal_states.append((next_player, b))
                legal_moves.append(i)
        return legal_states, legal_moves

    def neighbours(self, cell_indx):
        c = cell_indx % self.size
        r = cell_indx // self.size
        neighbours = [(r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c)]
        remove_elements = set()
        if r == 0:
            # don't add row above
            remove_elements.update([0, 1])
        elif r == self.size - 1:
            # don't add row below
            remove_elements.update([4, 5])
        if c == 0:
            # don't add column before
            remove_elements.update([2, 4])
        elif c == self.size - 1:
            # don't add column after
            remove_elements.update([1, 3])
        neighbours = [n[0]*self.size + n[1] for i, n in enumerate(neighbours) if i not in remove_elements]
        return neighbours

    def winner(self, state_key):
        # return winner (0 (no winner), 1 or 2)
        # need only to check if player won
        # player 1 should span all rows (top-bottom)
        # player 2 should span all columns (left-right)
        # check if previous player won. subtract 1 from player to use as index
        player = (1 if state_key[0] == 2 else 2) - 1
        board = state_key[1]
        # iterates left to right and top to bottom
        if player == 0:
            to_visit = [i for i in range(self.size) if board[i][player] == 1]
        else:
            to_visit = [i for i in range(0, self.size**2, self.size) if board[i][player] == 1]
        # print("to_visit:", to_visit)
        to_visit = set(to_visit)

        prev_visit = set()
        while True:
            if not to_visit:
                break
            else:
                cell_indx = to_visit.pop()
                neighbours = [n for n in self.neighbours(cell_indx) if board[n][player] == 1 and n not in prev_visit]
                to_visit.update(neighbours)
                prev_visit.add(cell_indx)

        # check if right or bottom cells is in list depending on player
        if player == 0:
            goal = [i for i in range(self.size*(self.size-1), self.size**2)]
        else:
            goal = [i for i in range(self.size-1, self.size**2, self.size)]
        # print("goal:", goal)
        # print("prev_visit", prev_visit)
        for g in goal:
            if g in prev_visit:
                return player + 1
        # if no return, no winner
        return 0


if __name__ == '__main__':
    s_m = state_manager_hex(3, 1)
    states = [(2, [(0, 0), (0, 0), (0, 1), (0, 0), (1, 0), (1, 0), (0, 1), (0, 0), (1, 0)]),
                (1, [(0, 0), (0, 1), (0, 1), (0, 0), (1, 0), (1, 0), (0, 1), (0, 0), (1, 0)]),
                (2, [(1, 0), (0, 1), (0, 1), (0, 0), (1, 0), (1, 0), (0, 1), (0, 0), (1, 0)]),
                (1, [(1, 0), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (0, 1), (0, 0), (1, 0)]),
                (2, [(1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (1, 0)])]
    for state in states:
        print(state)
        print(s_m.print_board(state))
        print("winner:", s_m.winner(state))
