

from random import choice, randint, random


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
        if not Helper.__avoid_repetition_excessive(word) and not Helper.__avoid_word_in_dictionary(word, dictionnaire):
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


