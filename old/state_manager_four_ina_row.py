class state_manager_four_ina_row:
    # board representation:
    # 0 for no piece
    # 1 for player_1 piece
    # 2 for player_2 piece

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.start_player = 1

    def get_start(self):
        # returns start state
        return (self.start_player, [[0 for x in range(self.size_x)] for y in range(self.size_y)])

    def get_child_state_keys(self, state_key):
        # must return a list of unique keys for all child states
        player = 1 if state_key[0] == 2 else 2
        keys = []
        for x in range(self.size_x):
            # add piece on top for player
            keys.append(player, board)
