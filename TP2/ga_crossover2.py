import random
import yaml
from helper import Helper


class GA_crossover2:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            documents = list(yaml.safe_load_all(file))
        self.parameters_ga = documents[0]['parameters_ga']
        self.elitisme = self.parameters_ga['elitisme']
        self.number_of_elitisme = self.parameters_ga['number_of_elitisme']
        self.etalon = self.parameters_ga['etalon']
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
        self.generation = self.parameters_ga['generation']
        self.selection_method = self.parameters_ga['selection_method']


    def crossover_multi_points(self, words, trigram_model, dictionnaire, etalon=None):
        results = []
        losers = []
        safety_counter = 0
        while True:
            if self.etalon == True and etalon is not None:
                parent1 = etalon
            else:
                parent1 = Helper.select_parent(self.parameters_ga['selection_method'], words, trigram_model=trigram_model)
            parent2 = Helper.select_parent(self.parameters_ga['selection_method'], words, trigram_model=trigram_model)
            max_len = min(len(parent1), len(parent2))
            for _ in range(self.number_of_children):
                point1, point2, point3= sorted(random.sample(range(1, max_len), 3))
                if random.random() < self.crossover_rate:
                    child = (
                        parent1[:point1] +
                        parent2[point1:point2] +
                        parent1[point2:]
                    )
                else:
                    child = (
                        parent2[:point1] +
                        parent1[point1:point2] +
                        parent2[point2:point3] +
                        parent1[point3:point1] 
                    )

                child_results = Helper.calculate_perplexity(child, trigram_model)

                if child_results < self.franciosite and Helper.is_valid_word(child, dictionnaire):
                    # print(f"{child}: {child_results}")
                    results.append(child)

                if self.losers and child_results <= self.losers_franciosite and Helper.is_valid_word(child, dictionnaire):
                    # print(f"{child}: {child_results} - LOSER")
                    losers.append(child)
                
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
                        etalon = results[0]
                        for i in range(1, len(results)):
                            if Helper.calculate_perplexity(results[i], trigram_model) < Helper.calculate_perplexity(etalon, trigram_model):
                                etalon = results[i]
                        self.crossover_multi_points(results, trigram_model, dictionnaire, etalon=etalon)
                    else:
                        self.crossover_multi_points(results, trigram_model, dictionnaire)
