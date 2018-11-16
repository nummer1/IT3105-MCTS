import actors
import MCTS
import state_manager_hex
import threading


class GameGenerator(threading.Thread):
    # generate games
    def __init__(self, start_player, state_manager, actor, replay_buffer, lock, end_event, sim_time):
        threading.Thread.__init__(self)
        self.start_player = start_player
        self.state_manager = state_manager
        self.actor = actor
        self.replay_buffer = replay_buffer
        self.lock = lock
        self.end_event = end_event
        self.sim_time = sim_time

    def run(self):
        self.generate_games()

    def generate_games(self):
        # geenrate a game and add to replay_buffer
        while True:
            board = self.state_manager.get_start()
            MC = MCTS.MonteCarlo(self.start_player, self.state_manager, self.actor)
            while True:
                # Do M rollouts
                MC.search(sim_time=self.sim_time)
                distribution = MC.get_move_distribution()
                # lock before accesing shared replay_buffer
                self.lock.aquire()
                self.replay_buffer.append((board, distribution))
                self.lock.release()
                # Get next state based on rollouts
                board, move = MC.best_move()
                winner = self.state_manager.winner(board)
                # set new root
                MC.purge_tree(board)

                if winner != 0:
                    break
            # lock before accessing shared actor
            self.lock.aquire()
            self.actor.train_network(self.replay_buffer)
            self.lock.release()

            if self.end_event.is_set():
                # end_event is set to True when enough games are generated
                return

            if i in snapshots:
                actor.save(str(i))
