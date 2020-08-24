import re, json
from pprint import pprint

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


def process_duplicates(streets):
    """
    élimine les doublons (liens multiples sur une)
    gère l'appartenance éventuelle d'une rue à de multiples arrondissements
    """

    # print("before :", len(streets))
    # streets = set(streets)
    # print("after :", len(streets))

    singles = []
    dups = []
    for street in streets:
        if street in singles: 
            dups.append(street)
        else:
            singles.append(street)
    print("singles :", len(singles))
    print("dups :", len(dups))

    streets = singles

    already_seen = set()
    uniques = dict()

    for street in streets:

        arr, name, href = street

        name = name.replace(".", "")
        name = name.replace("-", " ")

        try:
            name = name.replace(" (Paris)", "")
        except:
            pass

        if name in already_seen:
            uniques[name]['arr'].append(arr)
        else:
            uniques[name] = {   'arr' : [arr],
                                'href' : href}
            already_seen.add(name)

    # build a list of records (dicts)

    list_of_uniques = []

    for name, value in uniques.items():
        key = normalize(name)
        d = dict()
        d['name'] = name
        d['key'] = build_key(name)
        d['arr'] = value["arr"]
        d['href'] = value['href']

        list_of_uniques.append(d)

    return list_of_uniques

def main():

    with open("out/list_of_streets.txt") as f:
        data = f.readlines()

    print(len(data))

    streets = []
    for l in data:
        # print(l)
        arr, name, href = l.strip().split(' # ')
        streets.append( (arr, name, href))

    print(streets[:10])

    uniques = process_duplicates(streets)

    with open("out/wkpd_streets.json", mode='w', encoding="utf8") as f:
        json.dump(uniques, f)


if __name__ == "__main__":
    main()

