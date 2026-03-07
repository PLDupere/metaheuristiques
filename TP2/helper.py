from nltk.probability import FreqDist
from random import choice, randint
import random
import csv
import gen_lm


class Helper:

    @staticmethod
    def generate_words(longueur_min=4, longueur_max=16, number_of_words=500, dictionnaire=None):
        start_symbol = "<s>"
        end_symbol = "</s>"
        valid_words = []

        while len(valid_words) < number_of_words:
            word_length = randint(longueur_min, longueur_max)
            word = ''.join(choice(Helper.get_alphabet()) for _ in range(word_length))
            if Helper.is_valid_word(word, dictionnaire):
                valid_words.append(word)
        return valid_words


    @staticmethod
    def is_valid_word(word, dictionnaire):
        if not Helper.__avoid_repetition_excessive(word) and not Helper.__avoid_word_in_dictionary(word, dictionnaire) and len(word) >= 4 and len(word) <= 16:
            return True
        return False


    @staticmethod
    def __avoid_repetition_excessive(word):
        for i in range(len(word) - 2):
            if word[i] == word[i + 1] == word[i + 2]:
                return True
        return False


    @staticmethod
    def __avoid_word_in_dictionary(word, dictionnaire):
        if dictionnaire is not None:
            return word in dictionnaire
        return False


    @staticmethod
    def get_alphabet():
        alphabet_autorise = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
            # 'é', 'è', 'ê', 'ë', 'û', 'ç', 'à', 'ô', 'î'
        ]
        return alphabet_autorise


    @staticmethod
    def build_letter_probabilities(words, alphabet):
        letters = []
        for w in words:
            letters.extend(list(w))
        fdist = FreqDist(letters)
        total = sum(fdist.values())
        probs = []
        for letter in alphabet:
            probs.append(fdist[letter] / total if total > 0 else 0)
        return probs


    @staticmethod
    def save_results(results, output_file):
        with open(output_file, 'a') as f:
            for word in results:
                f.write(f"{word}\n")


    @staticmethod
    def calculate_perplexity(word, trigram_model):
        return gen_lm.perplexité(mot=word, trigram_model=trigram_model)


    @staticmethod
    def save_results(algorithme, results, output_file, trigram_model):
        with open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['algorithme', 'mot', 'valeur'])
            for mot in results:
                value = Helper.calculate_perplexity(mot, trigram_model)
                writer.writerow([algorithme, mot, value])


    @staticmethod
    def tournament_selection(words, tournament_size=3, trigram_model=None):
        selected = random.choices(words, k=tournament_size)
        parent = min(selected, key=lambda word: Helper.calculate_perplexity(word, trigram_model))
        return parent


    @staticmethod
    def wheel_selection(words, trigram_model=None):
        perplexities = [Helper.calculate_perplexity(word, trigram_model) for word in words]
        fitness = [1 / p for p in perplexities]
        total_fitness = sum(fitness)
        probabilities = [f / total_fitness for f in fitness]
        parent = random.choices(words, weights=probabilities)[0]
        return parent


    @staticmethod
    def rank_selection(words, trigram_model=None):
        ranked_words = sorted(words, key=lambda word: Helper.calculate_perplexity(word, trigram_model))
        total_ranks = sum(range(1, len(ranked_words) + 1))
        probabilities = [(len(ranked_words) - i) / total_ranks for i in range(len(ranked_words))]
        parent = random.choices(ranked_words, weights=probabilities)[0]
        return parent
