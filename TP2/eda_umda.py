import yaml
import random
from helper import Helper


class EDA_UMDA:

    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            documents = list(yaml.safe_load_all(file))
        self.parameters_eda = documents[1]['parameters_eda']
        self.population_size = self.parameters_eda['population_size']
        self.selection_ratio = self.parameters_eda['selection_ratio']
        self.learning_rate = self.parameters_eda['learning_rate']
        self.franciosite = self.parameters_eda['franciosite']
        self.output_file = self.parameters_eda['output_file']
        self.min_word_length = 4
        self.max_word_length = 16
        self.alphabet = Helper.get_alphabet()
        self.alphabet_size = len(self.alphabet)
        self.letter_to_idx = {c: i for i, c in enumerate(self.alphabet)}

    def UMDA(self, words, trigram_model, dictionnaire):
        population = [(w, Helper.calculate_perplexity(w, trigram_model)) for w in words]
        population = sorted(population, key=lambda x: x[1])[:self.population_size]
        results = []

        base_probs = Helper.build_letter_probabilities(
            [w for w, _ in population], self.alphabet
        )
        prob_vector = [base_probs.copy() for _ in range(self.max_word_length)]

        while True:
            num_selected = int(self.population_size * self.selection_ratio)
            selected = population[:num_selected]
            for pos in range(self.max_word_length):
                counts = [0] * self.alphabet_size
                valid_words = 0
                for word, _ in selected:
                    if pos < len(word):
                        letter = word[pos]
                        idx = self.letter_to_idx[letter]
                        counts[idx] += 1
                        valid_words += 1

                if valid_words == 0:
                    continue

                for i in range(self.alphabet_size):
                    marginal_prob = counts[i] / valid_words
                    prob_vector[pos][i] = (
                        (1 - self.learning_rate) * prob_vector[pos][i]
                        + self.learning_rate * marginal_prob
                    )

            new_population = []
            for _ in range(self.population_size):
                length = random.randint(self.min_word_length, self.max_word_length)
                word_list = []
                for pos in range(length):
                    letter = random.choices(
                        self.alphabet,
                        weights=prob_vector[pos]
                    )[0]
                    word_list.append(letter)

                word = ''.join(word_list)
                fitness = Helper.calculate_perplexity(word, trigram_model)
                new_population.append((word, fitness))

            population = sorted(new_population, key=lambda x: x[1])
            for word, fitness in population:
                if fitness < self.franciosite and Helper.is_valid_word(word, dictionnaire):
                    print(f"{word}: {fitness}")
                    results.append(word)

            if len(results) >= self.population_size:
                Helper.save_results("UMDA", results, self.output_file, trigram_model)
                return results[:self.population_size]

