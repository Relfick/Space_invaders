import torch
import random


class Genetic:
    def __init__(self, bots: list, av_time_lived):
        self.bots = bots
        self.fitnesses = [bot.player.time_lived for bot in self.bots]
        self.n_input, self.n_hidden_1, self.n_hidden_2, self.n_output, self.layers_num = self.bots[0].get_net_structure()
        self.neurons_num_in_layers = [self.n_input, self.n_hidden_1, self.n_hidden_2, self.n_output]
        self.boundaries = []
        self.genomes = []
        self.selection()
        self.store_genomes()
        self.crossover()
        self.mutation()
        self.refresh_bots()


    def selection(self):
        self.bots.sort(key=lambda fit: fit.player.time_lived, reverse=True)

    def store_genomes(self):
        for bot in self.bots:
            genome = []
            for layer in bot.net.layers:
                weight = layer.weight
                bias = layer.bias
                genome.append(torch.cat((weight, bias.unsqueeze(1)), 1))
            self.genomes.append(genome)

    def create_children_genomes(self, parent1, parent2):
        child1 = []
        child2 = []
        for i in range(self.layers_num):
            child1.append(torch.cat((parent1[i][:self.boundaries[i]], parent2[i][self.boundaries[i]:]), 0))
            child2.append(torch.cat((parent2[i][:self.boundaries[i]], parent1[i][self.boundaries[i]:]), 0))
        return child1, child2

    def crossover(self):
        if random.random() * 100 > 90:
            return

        self.boundaries = []
        for n in self.neurons_num_in_layers[1:]: # 1: потому что инпут слой не учитывается
            bound = (random.random() - 0.5) / 2 + 0.5
            bound = round(n * bound)
            self.boundaries.append(bound)

        self.genomes[-1], self.genomes[-2] = self.create_children_genomes(self.genomes[0], self.genomes[1])
        self.genomes[-3], self.genomes[-4] = self.create_children_genomes(self.genomes[0], self.genomes[2])
        self.genomes[-5], self.genomes[-6] = self.create_children_genomes(self.genomes[1], self.genomes[2])

        # boundary1 = (random.random() - 0.5) / 2 + 0.5
        # boundary1 = round(self.n_hidden * boundary1)
        # boundary2 = (random.random() - 0.5) / 2 + 0.5
        # boundary2 = round(self.n_hidden * boundary2)
        # boundary3 = (random.random() - 0.5) / 2 + 0.5
        # boundary3 = round(self.n_output * boundary3)
        #
        # # new_genomexy: x - net layer number, y - child number
        # new_genome11 = torch.cat((self.genomes[0][0][:boundary1], self.genomes[1][0][boundary1:]), 0)
        # new_genome21 = torch.cat((self.genomes[0][1][:boundary2], self.genomes[1][1][boundary2:]), 0)
        # new_genome31 = torch.cat((self.genomes[0][2][:boundary3], self.genomes[1][2][boundary3:]), 0)
        #
        # new_genome12 = torch.cat((self.genomes[1][0][:boundary1], self.genomes[0][0][boundary1:]), 0)
        # new_genome22 = torch.cat((self.genomes[1][1][:boundary2], self.genomes[0][1][boundary2:]), 0)
        #
        # new_genome13 = torch.cat((self.genomes[0][0][:boundary1], self.genomes[2][0][boundary1:]), 0)
        # new_genome23 = torch.cat((self.genomes[0][1][:boundary2], self.genomes[2][1][boundary2:]), 0)
        #
        # new_genome14 = torch.cat((self.genomes[2][0][:boundary1], self.genomes[0][0][boundary1:]), 0)
        # new_genome24 = torch.cat((self.genomes[2][1][:boundary2], self.genomes[0][1][boundary2:]), 0)
        #
        # new_genome15 = torch.cat((self.genomes[1][0][:boundary1], self.genomes[2][0][boundary1:]), 0)
        # new_genome25 = torch.cat((self.genomes[1][1][:boundary2], self.genomes[2][1][boundary2:]), 0)
        #
        # new_genome16 = torch.cat((self.genomes[2][0][:boundary1], self.genomes[1][0][boundary1:]), 0)
        # new_genome26 = torch.cat((self.genomes[2][1][:boundary2], self.genomes[1][1][boundary2:]), 0)
        #
        # self.genomes[-1] = [new_genome11, new_genome21]
        # self.genomes[-2] = [new_genome12, new_genome22]
        # self.genomes[-3] = [new_genome13, new_genome23]
        # self.genomes[-4] = [new_genome14, new_genome24]
        # self.genomes[-5] = [new_genome15, new_genome25]
        # self.genomes[-6] = [new_genome16, new_genome26]

    def mutation(self):
        for genome in self.genomes:
            for i in range(self.layers_num):
                self.mutate_genome(genome[i])

    def mutate_genome(self, genome):
        mutation_prob = 10
        for i in range(genome.shape[0]):
            max_gen = genome[i].max()
            min_gen = genome[i].min()
            for j in range(genome.shape[1]):
                if random.random() * 100 < mutation_prob:
                    genome[i][j] = self.mutation_fun2(max_gen, min_gen, genome[i][j])

    def mutation_fun1(self, max_gen, min_gen, gen):
        return min_gen + max_gen - gen

    def mutation_fun2(self, max_gen, min_gen, gen):
        span = float(max_gen - min_gen)
        delta_gen = span / 5
        r = random.random()
        if random.random() > 0.5:
            if gen + delta_gen < max_gen:
                return gen + r * delta_gen
            else:
                return gen - r * delta_gen
        else:
            if gen - delta_gen > min_gen:
                return gen - r * delta_gen
            else:
                return gen + r * delta_gen

    def refresh_bots(self):
        for i in range(len(self.bots)):
            weights = []
            biases = []
            for j in range(self.layers_num):
                weights.append(self.genomes[i][j][:, :-1])
                biases.append(self.genomes[i][j][:, -1])
            self.bots[i].set_net_parameters(weights, biases)

    def get_bots(self):
        return self.bots
