import re
from difflib import SequenceMatcher

TRTAB = str.maketrans("’ÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸàâãäáçéèêëìíîïñòóôõöùúûüýÿž", "'aaaceeeeiioouuuyaaaaaceeeeiiiinooooouuuuyyz")
LIGATURES = { "Æ" : "ae", "Œ": "oe", "æ" : "ae", "œ" : "oe"}

def remove_spaces(string):
    return string.replace(" ", "")

def normalize(word):
    """
    retourne une string normalisée (minuscules, remplacement des caractères spéciaux, etc...)
    """
    for k,v in LIGATURES.items():
        try:
            word = word.replace(k, v)
        except:
            pass

    return word.translate(TRTAB).lower()

def shorten(word):

    try:
        word = word.replace("-", " ")
    except:
        pass

    try:
        word = word.replace("'", " ")
    except:
        pass

    return word



def build_key(string):
    return remove_spaces(shorten(normalize(string)))


def is_matching(word, pattern):
    """
    retourne la vérité de "word MATCH pattern" au sens du package re
    """
    return pattern.match(word)


def is_similar(a, b, ratio):
    """
    retourne la vérité de "a est similaire à b"
    """
    return SequenceMatcher(None, a, b).ratio() > ratio
