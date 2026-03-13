import random
import yaml
from helper import Helper


class GA_crossover1:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            documents = list(yaml.safe_load_all(file))
        self.parameters_ga = documents[0]['parameters_ga']
        self.generation = self.parameters_ga['generation']
        self.etalon = self.parameters_ga['etalon']
        self.elitisme = self.parameters_ga['elitisme']
        self.number_of_elitisme = self.parameters_ga['number_of_elitisme']
        self.losers = self.parameters_ga['losers']
        self.losers_franciosite = self.parameters_ga['losers_franciosite']
        self.number_of_losers = self.parameters_ga['number_of_losers']
        self.reseed = self.parameters_ga['reseed']
        self.number_of_reseeds = self.parameters_ga['number_of_reseeds']
        self.mutation_rate = self.parameters_ga['mutation_rate']
        self.franciosite = self.parameters_ga['franciosite']
        self.franciosite_diminution_by_generation = self.parameters_ga['franciosite_diminution_by_generation']
        self.population_size = self.parameters_ga['population_size']
        self.number_of_children = self.parameters_ga['number_of_children']
        self.crossover_rate = self.parameters_ga['crossover_rate']
        self.selection_method = self.parameters_ga['selection_method']


    def crossover_single_point(self, words, trigram_model, dictionnaire, etalon=None):
        results = []
        losers = []
        children = []
        safety_counter = 0
        while True:
            if self.etalon == True and etalon is not None:
                parent1 = etalon
            else:
                parent1 = Helper.select_parent(self.parameters_ga['selection_method'], words, trigram_model=trigram_model)
            parent2 = Helper.select_parent(self.parameters_ga['selection_method'], words, trigram_model=trigram_model)

            for _ in range(self.number_of_children):
                point = random.randint(1, len(parent1) - 1)
                if random.random() < 0.5:
                    child = parent1[:point] + parent2[point:]
                else:
                    child = parent2[:point] + parent1[point:]
                children.append(child)

                for i in children:
                    child_results = Helper.calculate_perplexity(i, trigram_model)
                    if child_results < self.franciosite and Helper.is_valid_word(i, dictionnaire):
                        # print(f"{i}: {child_results}")
                        results.append(i)
                        continue
                    if self.losers and child_results <= self.losers_franciosite and Helper.is_valid_word(i, dictionnaire):
                        # print(f"{i}: {child_results} - LOSER")
                        losers.append(i)
                children = []
                safety_counter += 1

                if len(results) >= self.population_size or safety_counter > 10000:
                    if self.generation == 0:
                        return results
                    else:
                        if self.elitisme == True:
                            sorted_results = sorted(results, key=lambda word: Helper.calculate_perplexity(word, trigram_model))
                            results = sorted_results[:self.number_of_elitisme]
                        if self.reseed == True:
                            seeds = Helper.generate_words(4,16, self.number_of_reseeds, dictionnaire)
                            results.extend(seeds)
                        if self.losers == True and len(losers) > 0:
                            for _ in range(min(self.number_of_losers, len(losers))):
                                results.insert(random.randint(0, len(results)), random.choice(losers))
                        self.generation = self.generation - 1
                        self.franciosite = self.franciosite - self.franciosite_diminution_by_generation
                        if self.etalon == True:
                            etalon = results[0] if results else None
                            for i in range(1, len(results)):
                                if Helper.calculate_perplexity(results[i], trigram_model) < Helper.calculate_perplexity(etalon, trigram_model):
                                    etalon = results[i]
                            self.crossover_single_point(results, trigram_model, dictionnaire, etalon=etalon)
                        else:
                            self.crossover_single_point(results, trigram_model, dictionnaire)
