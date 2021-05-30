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

    def set_net_parameters(self, weight1, bias1, weight2, bias2):
        self.net.fc1.weight = torch.nn.Parameter(weight1)
        self.net.fc1.bias = torch.nn.Parameter(bias1)
        self.net.fc2.weight = torch.nn.Parameter(weight2)
        self.net.fc2.bias = torch.nn.Parameter(bias2)

    def set_player(self, player):
        self.player = player
