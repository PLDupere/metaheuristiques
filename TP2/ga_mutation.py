import random
import yaml
from helper import Helper


class GA_mutation:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            documents = list(yaml.safe_load_all(file))
        self.parameters_ga = documents[0]['parameters_ga']
        self.elitisme = self.parameters_ga['elitisme']
        self.etalon = self.parameters_ga['etalon']
        self.losers = self.parameters_ga['losers']
        self.number_of_loosers = self.parameters_ga['number_of_loosers']
        self.reseed = self.parameters_ga['reseed']
        self.number_of_reseeds = self.parameters_ga['number_of_reseeds']
        self.mutation_rate = self.parameters_ga['mutation_rate']
        self.franciosite = self.parameters_ga['franciosite']
        self.franciosite_diminution_by_generation = self.parameters_ga['franciosite_diminution_by_generation']
        self.population_size = self.parameters_ga['population_size']
        self.number_of_children = self.parameters_ga['number_of_children']
        self.crossover_rate = self.parameters_ga['crossover_rate']
        self.output_file = self.parameters_ga['output_file']


    def mutation(self, words, trigram_model, dictionnaire, etalon=None, iteration=0):
        results = []
        losers = []
        while True:
            if self.etalon == True and etalon is not None:
                parent1 = etalon
            else:
                parent1 = Helper.rank_selection(words, trigram_model=trigram_model)
            parent2 = Helper.rank_selection(words, trigram_model=trigram_model)

            avg_length = (len(parent1) + len(parent2)) / 2
            num_mutations = int(avg_length * self.mutation_rate)

            for _ in range(self.number_of_children):
                parent = random.choice([parent1, parent2])
                other_parent = parent2 if parent == parent1 else parent1
                mutated_child = list(parent)
                for _ in range(num_mutations):
                    if random.random() < self.mutation_rate:
                        index = random.randint(0, len(mutated_child) - 1)
                        random_char = random.choice(other_parent[::-1])
                        mutated_child[index] = random_char

                child = ''.join(mutated_child)
                child_results = Helper.calculate_perplexity(child, trigram_model)
                if child_results < self.franciosite and Helper.is_valid_word(child, dictionnaire):
                    print(f"{child}: {child_results}")
                    results.append(child)
                if self.losers == True and child_results <= self.franciosite + 5 and Helper.is_valid_word(child, dictionnaire):
                    print(f"{child}: {child_results}")
                    losers.append(child)

            if len(results) >= self.population_size:
                if self.elitisme == 0:
                    Helper.save_results("Mutation", results, self.output_file, trigram_model)
                    return results
                else:
                    if self.reseed == True:
                        seeds = Helper.generate_words(4,16, self.number_of_reseeds, dictionnaire)
                        results.extend(seeds)
                    if self.losers == True and len(losers) > 0:
                        for _ in range(min(self.number_of_loosers, len(losers))):
                            results.insert(random.randint(0, len(results)), random.choice(losers))
                    self.elitisme = self.elitisme - 1
                    self.franciosite = self.franciosite - self.franciosite_diminution_by_generation
                    if self.etalon == True:
                        etalon = results[0]
                        for i in range(1, len(results)):
                            if Helper.calculate_perplexity(results[i], trigram_model) < Helper.calculate_perplexity(etalon, trigram_model):
                                etalon = results[i]
                        self.mutation(results, trigram_model, dictionnaire, etalon=etalon)
                    else:
                        self.mutation(results, trigram_model, dictionnaire)
