from bs4 import BeautifulSoup
import requests
import json
import re

TRTAB = str.maketrans("’ÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸàâãäáçéèêëìíîïñòóôõöùúûüýÿž", "'aaaceeeeiioouuuyaaaaaceeeeiiiinooooouuuuyyz")
LIGATURES = { "Æ" : "ae", "Œ": "oe", "æ" : "ae", "œ" : "oe"}

def normalize(word):
    """
    retourne une string normalisée (minuscules, remplacement des caractères spéciaux, etc...)
    """
    for k,v in LIGATURES.items():
        try:
            word = word.replace(k, v)
        except:
            pass

    try:
        word = word.replace("-", " ")
    except:
        pass

    return word.translate(TRTAB).lower()

BASE_URL = "https://fr.wikipedia.org/wiki/"

ARRS = [ i+1 for i in range(20)]

STREETS_BY_ARR = {  1 : "Liste_des_voies_du_1er_arrondissement_de_Paris",
                    2 : "Liste_des_voies_du_2e_arrondissement_de_Paris",
                    3 : "Liste_des_voies_du_3e_arrondissement_de_Paris",
                    4 : "Liste_des_voies_du_4e_arrondissement_de_Paris",
                    5 : "Liste_des_voies_du_5e_arrondissement_de_Paris",
                    6 : "Liste_des_voies_du_6e_arrondissement_de_Paris",
                    7 : "Liste_des_voies_du_7e_arrondissement_de_Paris",
                    8 : "Liste_des_voies_du_8e_arrondissement_de_Paris",
                    9 : "Liste_des_voies_du_9e_arrondissement_de_Paris",
                    10 : "Liste_des_voies_du_10e_arrondissement_de_Paris",
                    11 : "Liste_des_voies_du_11e_arrondissement_de_Paris",
                    12 : "Liste_des_voies_du_12e_arrondissement_de_Paris",
                    13 : "Liste_des_voies_du_13e_arrondissement_de_Paris",
                    14 : "Liste_des_voies_du_14e_arrondissement_de_Paris",
                    15 : "Liste_des_voies_du_15e_arrondissement_de_Paris",
                    16 : "Liste_des_voies_du_16e_arrondissement_de_Paris",
                    17 : "Liste_des_voies_du_17e_arrondissement_de_Paris",
                    18 : "Liste_des_voies_du_18e_arrondissement_de_Paris",
                    19 : "Liste_des_voies_du_19e_arrondissement_de_Paris",
                    20 : "Liste_des_voies_du_20e_arrondissement_de_Paris" }


def get_wkpd_html(url):
    url = BASE_URL + url
    r = requests.get(url)
    return r.text



def get_streets_by_arr(arr, html):
    soup = BeautifulSoup(html, "html.parser")

    # search for divs containing streets
    divs = soup.findAll("div", {"class": "colonnes"})

    # extract relative anchors
    anchors = []
    for div in divs:
        # print(div)
        # print()
        anchors.extend([ a for a in div.findAll("a") if a.has_attr('title')])
     # anchors.append(div.findAll("a"))

    # print(anchors)
    # print(len(anchors))

    # build corresponding dict
    d = dict()
    for a in anchors:
        # print(a)
        d[normalize(a['title'])] = { 'href':a['href'], 'arr': [arr] }
        # try:
        #     d[a['title']] = a['href']
        # except:
        #     pass

    # logging.info(d)

    return d


def process_duplicates(streets):
    """
    gère l'appartenance éventuelle d'une rue à de multiples arrondissements
    """

    already_seen = set()

    uniques = dict()

    for streets_by_arr in streets:

        for k in streets_by_arr.keys():
                if k not in already_seen:
                    uniques[k] = streets_by_arr[k]
                    already_seen.add(k)
                else:
                    uniques[k]['arr'].extend(streets_by_arr[k]['arr'])

    return uniques


def clean_keys(streets):

    # Les rues qui n'ont pas de page Wikipedia ont la chaîne de caractère " (Paris)".
    # On la retire
    # pattern = " (page inexistante)"

    # for k,v in streets.items():
    #     if pattern in k:
    #         new_k = k.replace(pattern, "")
    #         v['href'] = None
    #         streets[new_k] = v
    #         del streets[k]

    # Les rues qui existent également dans d'autres villes sont identifiées
    # avec la chaîne de caractère " (Paris)". On la retire
    pattern = " (Paris)"

    for k,v in streets.items():
        if pattern in k:
            new_k = k.replace(pattern, "")
            streets[new_k] = v
            del streets[k]


    # Le scraping extrait les années 1970 et 1991. On retire les entrées correspondantes

    wrongs = [ "1970", "1991"]
    for k in wrongs: del streets[k]


    return streets


def remove_streets(streets):

    p1 = re.compile(r"Voie \w+/\d+")

    # retire les voies sans nom
    keys_to_remove = []


    for k in streets.keys():
        
        if "inexistante" in k :
            keys_to_remove.append(k)
            continue
        
        if k == "Voie sans nom de Paris":
            keys_to_remove.append(k)
        
        if p1.match(k): keys_to_remove.append(k)
        # if p2.match(k):
        #     keys_to_remove.append(k)

    for k in keys_to_remove:
        del streets[k]


    return streets


def serialize(object, filename):

    with open(filename, mode="w", encoding="utf8") as f:
        json.dump(object, f, ensure_ascii=False)

def main():
    """
    parse les pages Wikipedia définies en tête de fichier pour produire
    un JSON des rues de Paris
    """
    streets = []

    for arr in ARRS:
        print(STREETS_BY_ARR[arr])
        html = get_wkpd_html(STREETS_BY_ARR[arr])
        streets_by_arr = get_streets_by_arr(arr, html) # dict
        streets.append(streets_by_arr)

    # élimine les rues recensées dans plusieurs arrondissements
    unique_streets = process_duplicates(streets) # dict

    # nettoie les clés
    wkpd_streets = clean_keys(unique_streets) # dict

    # élimine les voies sans nom
    clean_streets = remove_streets(wkpd_streets) # dict

    # sauvegarde le dictionnaire au format JSON
    serialize(clean_streets, "out_streets_from_wkpd.json")



if __name__ == "__main__":
    main()