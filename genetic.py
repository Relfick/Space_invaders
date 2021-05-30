import torch
import random
import numpy as np


class Genetic:
    def __init__(self, bots: list, max_num_enemies):
        self.bots = bots
        self.fitnesses = [bot.player.time_lived for bot in self.bots]
        self.genomes = []
        self.n_input = max_num_enemies * 2 + 2
        self.n_hidden = self.n_input * 2
        self.n_output = 4
        self.selection()
        self.store_genomes()
        self.crossover()
        self.mutation()
        self.refresh_bots()

    def selection(self):
        self.bots.sort(key=lambda fit: fit.player.time_lived, reverse=True)

    def store_genomes(self):
        for bot in self.bots:
            # weightx: x - net layer number
            weight1 = bot.net.fc1.weight  # size(n_hidden, n_input)
            bias1 = bot.net.fc1.bias  # size(1, n_hidden)
            genome1 = torch.cat((weight1, bias1.unsqueeze(1)), 1)

            weight2 = bot.net.fc2.weight  # size(n_output, n_hidden)
            bias2 = bot.net.fc2.bias  # size(1, n_output)
            genome2 = torch.cat((weight2, bias2.unsqueeze(1)), 1)

            self.genomes.append([genome1, genome2])

    def crossover(self):
        if random.random() * 100 > 90:
            return
        boundary1 = (random.random() - 0.5) / 2 + 0.5
        boundary1 = round(self.n_hidden * boundary1)
        boundary2 = (random.random() - 0.5) / 2 + 0.5
        boundary2 = round(self.n_output * boundary2)

        # new_genomexy: x - net layer number, y - child number
        new_genome11 = torch.cat((self.genomes[0][0][:boundary1], self.genomes[1][0][boundary1:]), 0)
        new_genome21 = torch.cat((self.genomes[0][1][:boundary2], self.genomes[1][1][boundary2:]), 0)

        new_genome12 = torch.cat((self.genomes[1][0][:boundary1], self.genomes[0][0][boundary1:]), 0)
        new_genome22 = torch.cat((self.genomes[1][1][:boundary2], self.genomes[0][1][boundary2:]), 0)

        self.genomes[-1] = [new_genome11, new_genome21]
        self.genomes[-2] = [new_genome12, new_genome22]

    def mutation(self):
        mutation_prob = 10
        for genome1, genome2 in self.genomes:
            for i in range(genome1.shape[0]):
                max_gen = genome1[i].max()
                min_gen = genome1[i].min()
                for j in range(genome1.shape[1]):
                    if random.random() * 100 < mutation_prob:
                        genome1[i][j] = self.mutation_fun(max_gen, min_gen, genome1[i][j])

            for i in range(genome2.shape[0]):
                max_gen = genome2[i].max()
                min_gen = genome1[i].min()
                for j in range(genome2.shape[1]):
                    if random.random() * 100 < mutation_prob:
                        genome2[i][j] = self.mutation_fun(max_gen, min_gen, genome2[i][j])

    def mutation_fun(self, max_gen, min_gen, gen):
        return min_gen + max_gen - gen

    def refresh_bots(self):
        for i in range(len(self.bots)):
            weight1 = self.genomes[i][0][:, :-1]
            bias1 = self.genomes[i][0][:, -1]
            weight2 = self.genomes[i][1][:, :-1]
            bias2 = self.genomes[i][1][:, -1]
            self.bots[i].set_net_parameters(weight1, bias1, weight2, bias2)

    def get_bots(self):
        return self.bots