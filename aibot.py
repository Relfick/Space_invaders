from network import Network
from player import Player


class AI():
    def __init__(self):
        self.net = Network()
        self.predictions = []

    def predict(self, x):
        self.predictions = self.net.forward(x)
        return [i > 0.5 for i in self.predictions]




