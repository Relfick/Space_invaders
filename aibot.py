import torch.nn

from network import Network


class Bot:
    def __init__(self, max_num_enemies, player=None):
        self.net = Network(max_num_enemies)
        self.predictions = []
        if player:
            self.player = player

    def predict(self, x):
        self.predictions = self.net.forward(x)
        return [i > 0.5 for i in self.predictions]

    def get_player(self):
        return self.player

    def set_net_parameters(self, weights, biases):
        for i in range(len(self.net.layers)):
            self.net.layers[i].weight = torch.nn.Parameter(weights[i])
            self.net.layers[i].bias = torch.nn.Parameter(biases[i])

    def set_player(self, player):
        self.player = player

    def get_net_structure(self):
        return self.net.get_structure()
