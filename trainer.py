import MCTS
import actors


class Trainer:
    # generate games
    def __init__(self, start_player, state_manager, actor, replay_buffer, verbose, name):
        self.start_player = start_player
        self.state_manager = state_manager
        self.actor = actor
        self.replay_buffer = replay_buffer
        self.verbose = verbose
        self.name = name

    def generate_games(self, episodes, snapshots, batch_size, sim_time=0, rollouts_per_move=0, generate_random=False):
        # geenrate a game and add to replay_buffer
        print("Net will be cahced after the following episodes:", snapshots)
        self.actor.save(self.name + "0")
        if generate_random:
            generator = actors.Random(self.state_manager)
        else:
            generator = self.actor
        for i in range(1, episodes + 1):
            board = self.state_manager.get_start()
            MC = MCTS.MonteCarlo(self.start_player, self.state_manager, generator)
            while True:
                # Do M rollouts
                MC.search(sim_time=sim_time, simulations=rollouts_per_move)
                distribution = MC.get_move_distribution()
                self.replay_buffer.append((board, distribution))
                # Get next state based on rollouts
                board, move = MC.best_move()
                winner = self.state_manager.winner(board)
                if self.verbose:
                    self.state_manager.print_move(move)
                    self.state_manager.print_board(board)
                # set new root
                MC.purge_tree(board)

                if winner != 0:
                    break
            # lock before accessing shared actor
            self.actor.train_network(self.replay_buffer, batch_size=batch_size)

            if i in snapshots:
                self.actor.save(self.name + str(i))
