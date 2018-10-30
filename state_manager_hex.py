import copy


# TODO: Implement disjoint-set datastructure

# class Board:
#     def __init__(self, size, player_turn):
#         self.size = size
#         self.player_turn = player_turn
#         self.board = [[Cell(r, c, self.get_neighbours(r, c)) for c in range(size)] for r in range(size)]
#         print(self.board)
#
#     def get_kid(self, row, col):
#         cp_board = copy.deepcopy(self)
#         cp_board[row][col].fill(self.player_turn)
#         cp_board.player_turn = 1 if cp_board.player_turn == 2 else 2
#
#     def get_legal_children(self):
#         children = []
#         for r, row in enumerate(self.board):
#             for c, cell in enumerate(row):
#                 if cell.is_empty():
#                     children.append(self.get_kid(r, c))
#
#     def get_neighbours(self, r, c):
#         # returns neighbours of (r, c)
#         neighbours = [(r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c)]
#         remove_elements = set()
#         if r == 0:
#             # don't add row above
#             remove_elements.update([0, 1])
#         elif r == self.size - 1:
#             # don't add row below
#             remove_elements.update([4, 5])
#         if c == 0:
#             # don't add column before
#             remove_elements.update([2, 4])
#         elif c == self.size - 1:
#             # don't add column after
#             remove_elements.update([1, 3])
#         neighbours = [self.board[n[0]][n[1]] for i, n in enumerate(neighbours) if i not in remove_elements]
#         return neighbours
#
#     def winner(self, player):
#         # adds a hex by player 1 or 2 at coordinate (row, col) and returns 0, 1 or 2 based on win
#         if player == 1:
#             for row in range(self.size):
#                 cell = self.board[row][self.size-1]
#                 if cell.is_connected_to_edge and cell.player == player:
#                     return 1
#         else:
#             for col in range(self.size):
#                 cell = self.board[self.size-1][col]
#                 if cell.is_connected_to_edge and cell.player == player:
#                     return 2
#         return 0


# class Cell:
#     def __init__(self, row, col, neighbours):
#         self.is_empty = True
#         self.row = row
#         self.col = col
#         # 0 indicates no player
#         self.player = 0
#         self.neighbours = neighbours
#         self.is_connected_to_edge = False
#
#     def fill(self, player):
#         self.is_empty = False
#         # owner of hex
#         self.player = player
#         self.set_initial_edge_connection()
#         if self.is_connected_to_edge:
#             self.update_connected_to_edge()
#
#     def set_initial_edge_connection(self):
#         if self.player == 1 and self.col == 0:
#             self.is_connected_to_edge = True
#         elif self.player == 2 and self.row == 0:
#             self.is_connected_to_edge = True
#         for n in self.neighbours:
#             if n.is_connected_to_edge:
#                 self.is_connected_to_edge = True
#                 break
#
#     def set_is_connected_to_edge(self):
#         # tracks if p1 hex is connecteed to left edge and p2 hex is connected to top edge
#         self.is_connected_to_edge = True
#         for n in self.neighbours:
#             if not n.is_connected_to_edge and n.player == self.player:
#                 n.set_is_connected_to_edge()


class state_manager_hex:
    def __init__(self, size, start_player):
        self.size = size
        self.start_player = start_player
        # player 1 should always move first, start_player should be 1
        if self.start_player != 1:
            print("WARNING: start_player is not 1")

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
                b = copy.deepcopy(board)
                if cur_player == 1:
                    b[i] = (1, 0)
                else:
                    b[i] = (0, 1)
                legal_states.append((next_player, b))
                legal_moves.append(i)
        return legal_states, legal_moves

    def winner(self, state_key):
        # return winner (0 (no winner), 1 or 2)
        # need only to check if player won
        # player 1 should connect from left to right (row)
        # player 2 should connect from top to bottom (column)
        # check if previous player won. subtract 1 from player to use as index
        player = 1 if state_key[0] == 2 else 2
        return state_key[1].winner(player)

    # def neighbours(self, cell_indx):
    #     c = cell_indx % self.size
    #     r = cell_indx // self.size
    #     neighbours = [(r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c)]
    #     remove_elements = set()
    #     if r == 0:
    #         # don't add row above
    #         remove_elements.update([0, 1])
    #     elif r == self.size - 1:
    #         # don't add row below
    #         remove_elements.update([4, 5])
    #     if c == 0:
    #         # don't add column before
    #         remove_elements.update([2, 4])
    #     elif c == self.size - 1:
    #         # don't add column after
    #         remove_elements.update([1, 3])
    #     neighbours = [n[0]*self.size + n[1] for i, n in enumerate(neighbours) if i not in remove_elements]
    #     return neighbours
    #
    # def winner(self, state_key):
    #     # return winner (0 (no winner), 1 or 2)
    #     # need only to check if player won
    #     # player 1 should connect from left to right (row)
    #     # player 2 should connect from top to bottom (column)
    #     # check if previous player won. subtract 1 from player to use as index
    #     player = (1 if state_key[0] == 2 else 2) - 1
    #     board = state_key[1]
    #     # iterates left to right and top to bottom
    #     if player == 0:
    #         to_visit = [i for i in range(0, self.size**2, self.size) if board[i][player] == 1]
    #     else:
    #         to_visit = [i for i in range(self.size) if board[i][player] == 1]
    #     to_visit = set(to_visit)
    #
    #     prev_visit = set()
    #     while True:
    #         if not to_visit:
    #             break
    #         else:
    #             cell_indx = to_visit.pop()
    #             neighbours = [n for n in self.neighbours(cell_indx) if board[cell_indx][player] == 1 and n not in prev_visit]
    #             to_visit.update(neighbours)
    #             prev_visit.add(cell_indx)
    #
    #     # check if right or bottom cells is in list depending on player
    #     if player == 0:
    #         goal = [i for i in range(self.size-1, self.size**2, self.size)]
    #     else:
    #         goal = [i for i in range(self.size*(self.size-1), self.size**2)]
    #     for g in goal:
    #         if g in prev_visit:
    #             return player + 1
    #     # if no return, no winner
    #     return 0
