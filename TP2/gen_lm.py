import numpy as np
import nltk
from nltk.lm.preprocessing import pad_both_ends
from nltk.lm.preprocessing import flatten
from nltk import FreqDist, ConditionalFreqDist


def build_trigram_model(text: list):
    """Entraine une "character-based trigram" à partir d'un corpus d'entrainement. 

    Args:
        text (list): Une liste de mots constituant le corpus d'entrainement du modèle de langage simple

    Returns:
        nltk.ConditionalFreqDist: le modèle de langage - en l'occurence une trigramme
    """
    text = list(flatten(pad_both_ends(sent, n=3) for sent in text))
    trigrams = nltk.trigrams(text)
    trigram_freq_dist = FreqDist(trigrams)
    trigram_model = ConditionalFreqDist()

    for trigram, count in trigram_freq_dist.items():
        trigram_model[trigram[:2]][trigram[2]] = count

    return trigram_model


def perplexité(mot: str, trigram_model: ConditionalFreqDist) -> float:
    """Fonction de calcul de la perplexité d'un mot.

    Args:
        mot (str): Le mot à évaluer
        trigram_model (ConditionalFreqDist): La trigramme permettant l'évaluation

    Returns:
        float : La perplexité du mot
    """
    mot = list(pad_both_ends(mot, n=3))
    trigrammes = nltk.trigrams(mot)
    log_prob_sum = 0
    n = 0

    for trigram in trigrammes:
        bigram = trigram[:2] # le contexte m_i-1,m_i-2
        car = trigram[2] # le m_i

        try:
            prob = trigram_model[bigram].freq(car)
            if prob > 0:
                log_prob_sum += np.log2(prob)
                n += 1
            else:
                log_prob_sum += np.log2(0.0000000001)
                n += 1
        except KeyError: # pas top si ça arrive -- on ne veut pas vraiment de zero prob
            # on peut faire quelquechose de 💩
            # ça veut aussi dire qu'on ne parle plus de vraiii probabilités... 
            log_prob_sum += np.log2(0.0000000001)
            n += 1
            continue

    if n > 0:
        entropie = -log_prob_sum / n
        return 2 ** entropie
    else:
        return np.inf # en gros, un mot impossible...
    

