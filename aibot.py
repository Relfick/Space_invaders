from network import Network


class Bot:
    def __init__(self, player, max_num_enemies):
        self.net = Network(max_num_enemies)
        self.predictions = []
        self.player = player

    def predict(self, x):
        self.predictions = self.net.forward(x)
        return [i > 0.5 for i in self.predictions]

    def get_player(self):
        return self.player




