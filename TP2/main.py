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


#%%
# voici une brève démonstration de l'utilisation du code fourni

dictionnaire = generate_corpus.generate_dictionary() # peut prendre un peu de temps

# dans notre cas, on va bâtir bêtement le corpus directement à partir du dictionnaire traité
corpus_entraînement = dictionnaire

trigram_model = gen_lm.build_trigram_model(corpus_entraînement)

words = Helper.generate_words(longueur_min=4, longueur_max=16, number_of_words=500, dictionnaire=dictionnaire)

ga_instance1 = GA("parameters.yaml")
ga_instance2 = GA("parameters.yaml")
ga_instance3 = GA("parameters.yaml")

mutation_results = ga_instance1.mutation(words, trigram_model, dictionnaire)

single_results = ga_instance2.crossover_single_point(words, trigram_model, dictionnaire)

multi_results= ga_instance3.crossover_multi_points(words, trigram_model, dictionnaire)


# eda_instance = EDA("parameters.yaml")


# mots = ['bonjour', 'jourbon', 'manger', 'aaaaa', 'allo', 'gfsaa']

# %%
# for mot in mots:
#     ppl = gen_lm.perplexité(mot=mot, trigram_model=trigram_model)
#     print(f"{mot}: {ppl}")

# %%
