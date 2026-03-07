from ga_mutation import GA_mutation
from ga_crossover1 import GA_crossover1
from ga_crossover2 import GA_crossover2
from eda_umda import EDA_UMDA
import gen_lm
import generate_corpus
from helper import Helper
import yaml

with open("parameters.yaml", 'r') as file:
    documents = list(yaml.safe_load_all(file))
number_of_iterations = documents[2]['parameters_general']['number_of_iterations']
number_of_words_to_generate = documents[2]['parameters_general']['number_of_words_to_generate']

for iteration in range(number_of_iterations):
    dictionnaire = generate_corpus.generate_dictionary()
    corpus_entraînement = dictionnaire
    trigram_model = gen_lm.build_trigram_model(corpus_entraînement)
    words = Helper.generate_words(longueur_min=4, longueur_max=16, number_of_words=number_of_words_to_generate, dictionnaire=dictionnaire)

    genetic_algorithm_mutation_tournament_selection = GA_mutation("parameters.yaml")
    genetic_algorithm_crossover_wheel_selection = GA_crossover1("parameters.yaml")
    genetic_algorithm_crossover_tournament_selection = GA_crossover2("parameters.yaml")
    estimation_distribution_algorithm_univariate_distribution_algorithm = EDA_UMDA("parameters.yaml")

    genetic_algorithm_mutation_tournament_selection.mutation(words, trigram_model, dictionnaire, iteration)
    genetic_algorithm_crossover_wheel_selection.crossover_single_point(words, trigram_model, dictionnaire, iteration)
    genetic_algorithm_crossover_tournament_selection.crossover_multi_points(words, trigram_model, dictionnaire, iteration)
    estimation_distribution_algorithm_univariate_distribution_algorithm.UMDA(words, trigram_model, dictionnaire, iteration)
