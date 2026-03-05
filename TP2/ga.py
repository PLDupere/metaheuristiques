import random
import yaml

class GA:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            documents = list(yaml.safe_load_all(file))
        self.parameters_ga = documents[0]['parameters_ga']
        self.mutation_rate = self.parameters_ga['mutation_rate']
        self.population_size = self.parameters_ga['population_size']

    def print_parameters(self):
        print("Paramètres GA:", self.mutation_rate, self.population_size)

    def mutation(self, words):
        mutated_word = list(random.choice(words))
        for i in range(len(mutated_word)):
            if random.random() < self.mutation_rate:
                mutated_word[i] = random.choice(self.words)
        return ''.join(mutated_word)

    def crossover_single_point(self, words):
        parent1 = random.choice(words)
        parent2 = random.choice(words)
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2


    
    def crossover_two_points(self, words):
        parent1 = random.choice(words)
        parent2 = random.choice(words)
        max_len = min(len(parent1), len(parent2))
        point1, point2 = sorted(random.sample(range(1, max_len), 2))

        child1 = (
            parent1[:point1] +
            parent2[point1:point2] +
            parent1[point2:]
        )

        child2 = (
            parent2[:point1] +
            parent1[point1:point2] +
            parent2[point2:]
        )

        return child1, child2