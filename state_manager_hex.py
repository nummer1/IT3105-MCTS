class state_manager_hex:
    def __init__(self, size, start_player):
        self.size = size
        # player 1 should always move first, start_player should be 1
        if self.start_player != 1:
            print("WARNING: start_player is not 1")
        self.start_player = start_player

    def get_start(self):
        # return start state
        board = ['00' for i in range(self.size**2)]
        print("DEBUG", board)
        return (self.start_player, int(''.join(board), 2))

    def get_child_state_keys(self, state_key):
        # must return a list of unique keys for all legal child states
        # returns state and moves made to get to the state
        legal_states = []
        legal_moves = []
        player = state_key[0]
        board = bin(state_key[1])
        for i in board:
            pass
        return legal_states, legal_moves

    def winner(self, state_key):
        # return winner (0 (no winner), 1 or 2)
        pass
