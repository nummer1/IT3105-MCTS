from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


PATH = "/home/kasparov/Documents/IT3105-MCTS/"


class HexPlayer:
    def __init__(self, board_size):
        self.board_size = board_size
        self.node_number = board_size**2
        self.model = None
        self.epochs = 10
        self.bs = 4
        self.create_network()

    def create_network(self):
        self.model = Sequential()
        self.model.add(Dense(50, activation='relu', input_shape=([self.node_number * 2])))
        # self.model.add(Dense(25, activation='relu'))
        # TODO: softmax over only empty legal moves/nodes
        # TODO: softmax can be problematic if two good moves
        self.model.add(Dense(self.node_number, activation='relu'))
        # try rmsprop
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.summary()

    def train_network(self, input, target):
        # TODO: do training, take more parameters
        return None
        # self.model.fit(input, target, epochs=self.epochs, batch_size=self.bs)

    def save_weights(self, number):
        filepath = PATH + "weights/" + number + ".hdf5"
        self.model.save_weights(filepath)

    def load_weights(self, number):
        filepath = PATH + "weights/" + number + ".hdf5"
        self.model.load_weights(filepath)

    # def get_distribution(self, input, target, player):
    #     prediction = self.model.predict([input, target])
    #     print("prediction from get_distribution:", prediction)
    #     return prediction
