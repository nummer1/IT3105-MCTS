from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class HexPlayer:
    def __init__(self, board_size):
        self.board_size = board_size
        self.node_number = board_size**2
        self.model = None
        self.epochs = 10
        self.bs = 64

    def create_network(self):
        self.model = Sequential()
        self.model.add(Dense(25, activation='relu', input_shape=(self.node_number)))
        self.model.add(Dense(25, activation='relu'))
        # TODO: softmax over only empty legal moves/nodes
        self.model.add(Dense(self.node_number, activation='softmax'))
        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.summary()

    def train_network(self, input, target):
        self.model.fit(input, target, epochs=self.epochs, batch_size=self.bs)

    def get_best_move(self, input, target, player):
        prediction = self.model.predict([input, target])
        # TODO: use prediction to find best move
        pred_move = None
        return pred_move