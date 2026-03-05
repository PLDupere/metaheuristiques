import random
import yaml

import gen_lm
from helper import Helper

class GA:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            documents = list(yaml.safe_load_all(file))
        self.parameters_ga = documents[0]['parameters_ga']
        self.elitisme = self.parameters_ga['elitisme']
        self.etalon = self.parameters_ga['etalon']
        self.losers = self.parameters_ga['losers']
        self.reseed = self.parameters_ga['reseed']
        self.mutation_rate = self.parameters_ga['mutation_rate']
        self.franciosite = self.parameters_ga['franciosite']
        self.population_size = self.parameters_ga['population_size']


    def mutation(self, words, trigram_model, dictionnaire, etalon=None):
        results = []
        while True:
            if self.etalon == True and etalon is not None:
                parent1 = etalon
            else:
                parent1 = random.choice(words)
            parent2 = random.choice(words)
            avg_length = (len(parent1) + len(parent2)) / 2
            num_mutations = int(avg_length * self.mutation_rate)
            mutated_child1 = list(parent1)
            mutated_child2 = list(parent2)

            for _ in range(num_mutations):
                if random.random() < self.mutation_rate:
                    index = random.randint(0, len(mutated_child1) - 1)
                    random_char = random.choice(parent2[::-1])
                    mutated_child1[index] = random_char

            for _ in range(num_mutations):
                if random.random() < self.mutation_rate: 
                    index = random.randint(0, len(mutated_child2) - 1)
                    random_char = random.choice(parent1[::-1])
                    mutated_child2[index] = random_char

            child1 = ''.join(mutated_child1)
            child2 = ''.join(mutated_child2)

            child1_results = gen_lm.perplexité(mot=child1, trigram_model=trigram_model)
            child2_results = gen_lm.perplexité(mot=child2, trigram_model=trigram_model)

            if child1_results < self.franciosite and Helper.is_valid_word(child1, dictionnaire):
                print(f"{child1}: {child1_results}")
                results.append(child1)
            if child2_results < self.franciosite and Helper.is_valid_word(child2, dictionnaire):
                print(f"{child2}: {child2_results}")
                results.append(child2)
            if len(results) >= self.population_size:
                if self.elitisme == 0:
                    return results
                else:
                    self.elitisme = self.elitisme - 1
                    self.franciosite = self.franciosite - 1
                    if self.etalon == True:
                        etalon = results[0]
                        for i in range(1, len(results)):
                            if gen_lm.perplexité(mot=results[i], trigram_model=trigram_model) < gen_lm.perplexité(mot=etalon, trigram_model=trigram_model):
                                etalon = results[i]
                        self.mutation(results, trigram_model, dictionnaire, etalon=etalon)
                    else:
                        self.mutation(results, trigram_model, dictionnaire)


    def crossover_single_point(self, words, trigram_model, dictionnaire, etalon=None):
        results = []
        while True:
            if self.etalon == True and etalon is not None:
                parent1 = etalon
            else:
                parent1 = random.choice(words)
            parent2 = random.choice(words)
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            child1_results = gen_lm.perplexité(mot=child1, trigram_model=trigram_model)
            child2_results = gen_lm.perplexité(mot=child2, trigram_model=trigram_model)
            if child1_results < self.franciosite and Helper.is_valid_word(child1, dictionnaire):
                print(f"{child1}: {child1_results}")
                results.append(child1)
            if child2_results < self.franciosite and Helper.is_valid_word(child2, dictionnaire):
                print(f"{child2}: {child2_results}")
                results.append(child2)
            if len(results) >= self.population_size:

                if self.elitisme == 0:
                    return results
                else:
                    self.elitisme = self.elitisme - 1
                    self.franciosite = self.franciosite - 1
                    if self.etalon == True:
                        etalon = results[0]
                        for i in range(1, len(results)):
                            if gen_lm.perplexité(mot=results[i], trigram_model=trigram_model) < gen_lm.perplexité(mot=etalon, trigram_model=trigram_model):
                                etalon = results[i]
                        self.mutation(results, trigram_model, dictionnaire, etalon=etalon)
                    else:
                        self.mutation(results, trigram_model, dictionnaire)


    def crossover_multi_points(self, words, trigram_model, dictionnaire, etalon=None):
        results = []
        while True:
            if self.etalon == True and etalon is not None:
                parent1 = etalon
            else:
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
            child1_results = gen_lm.perplexité(mot=child1, trigram_model=trigram_model)
            child2_results = gen_lm.perplexité(mot=child2, trigram_model=trigram_model)
            if child1_results < self.franciosite and Helper.is_valid_word(child1, dictionnaire):
                print(f"{child1}: {child1_results}")
                results.append(child1)
            if child2_results < self.franciosite and Helper.is_valid_word(child2, dictionnaire):
                print(f"{child2}: {child2_results}")
                results.append(child2)
            if len(results) >= self.population_size:
                if self.elitisme == 0:
                    return results
                else:
                    self.elitisme = self.elitisme - 1
                    self.franciosite = self.franciosite - 1
                    if self.etalon == True:
                        etalon = results[0]
                        for i in range(1, len(results)):
                            if gen_lm.perplexité(mot=results[i], trigram_model=trigram_model) < gen_lm.perplexité(mot=etalon, trigram_model=trigram_model):
                                etalon = results[i]
                        self.mutation(results, trigram_model, dictionnaire, etalon=etalon)
                    else:
                        self.mutation(results, trigram_model, dictionnaire)
