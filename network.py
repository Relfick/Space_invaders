import torch


class Network(torch.nn.Module):
    def __init__(self, max_num_enemies):
        super(Network, self).__init__()
        self.fc1 = torch.nn.Linear(max_num_enemies * 2 + 2, 20)
        self.ac1 = torch.nn.Sigmoid()
        self.fc2 = torch.nn.Linear(20, 4)
        self.ac2 = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.ac1(x)
        x = self.fc2(x)
        x = self.ac2(x)
        return x
