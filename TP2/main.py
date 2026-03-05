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

# for trigram, probability in trigram_model.items():
#     print(f"Trigram: {trigram}, Probability: {probability}")



words = Helper.generate_words(longueur_min=4, longueur_max=16, number_of_words=500, dictionnaire=dictionnaire)




ga_instance = GA("parameters.yaml")
ga_instance.print_parameters()

# mutation_result = ga_instance.mutation(words)
# print("Résultat de la mutation:", mutation_result)

cross_result_single = ga_instance.crossover_single_point(words)
print("Résultat du crossover à point unique:", cross_result_single)

cross_result_multi = ga_instance.crossover_two_points(words)
print("Résultat du crossover à points multiples:", cross_result_multi)

eda_instance = EDA("parameters.yaml")


mots = ['bonjour', 'jourbon', 'manger', 'aaaaa', 'allo']


# %%
for mot in mots:
    ppl = gen_lm.perplexité(mot=mot, trigram_model=trigram_model)
    print(f"{mot}: {ppl}")

# %%
