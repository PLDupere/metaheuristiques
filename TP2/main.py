#%%
import numpy as np
import nltk
from nltk.util import pad_sequence
from nltk.lm.preprocessing import pad_both_ends
from nltk.lm.preprocessing import flatten
from nltk import FreqDist, ConditionalFreqDist
from collections import defaultdict

from ga import GA
from eda import EDA
import gen_lm
import generate_corpus
from helper import Helper


dictionnaire = generate_corpus.generate_dictionary()
corpus_entraînement = dictionnaire
trigram_model = gen_lm.build_trigram_model(corpus_entraînement)

words = Helper.generate_words(longueur_min=4, longueur_max=16, number_of_words=500, dictionnaire=dictionnaire)

# ga_instance1 = GA("parameters.yaml")
# ga_instance2 = GA("parameters.yaml")
# ga_instance3 = GA("parameters.yaml")

# mutation_results = ga_instance1.mutation(words, trigram_model, dictionnaire)
# single_results = ga_instance2.crossover_single_point(words, trigram_model, dictionnaire)
# multi_results= ga_instance3.crossover_multi_points(words, trigram_model, dictionnaire)

eda_instance1 = EDA("parameters.yaml")

umda_result = eda_instance1.UMDA(words, trigram_model, dictionnaire)
print(f"UMDA Best: {umda_result}")


