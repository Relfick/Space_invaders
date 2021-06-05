import torch


class Network(torch.nn.Module):
    def __init__(self, max_num_enemies):
        super(Network, self).__init__()
        self.n_inputs = max_num_enemies * 2 + 1
        self.n_hidden_1 = 4 * self.n_inputs
        self.n_hidden_2 = 3 * self.n_inputs
        self.n_outputs = 2
        self.fc1 = torch.nn.Linear(self.n_inputs, self.n_hidden_1)
        self.ac1 = torch.nn.Sigmoid()
        self.fc2 = torch.nn.Linear(self.n_hidden_1, self.n_hidden_2)
        self.ac2 = torch.nn.Sigmoid()
        self.fc3 = torch.nn.Linear(self.n_hidden_2, self.n_outputs)
        self.ac3 = torch.nn.Sigmoid()
        self.layers = [self.fc1, self.fc2, self.fc3]

    def forward(self, x):
        x = self.fc1(x)
        x = self.ac1(x)
        x = self.fc2(x)
        x = self.ac2(x)
        x = self.fc3(x)
        x = self.ac3(x)
        return x

    def get_structure(self):
        return self.n_inputs, self.n_hidden_1, self.n_hidden_2, \
               self.n_outputs, len(self.layers)
