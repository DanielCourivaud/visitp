import json
import re
from difflib import SequenceMatcher
from collections import defaultdict


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

# lecture des données Open Data Paris

print("# Lecture de 'voie.geojson'")
with open("data/voie.geojson", mode="r", encoding="utf8") as f:
    voies_geojson = json.load(f)
voies = voies_geojson["features"] # type list(dict)
print("\t", len(voies), "entrées dans les données initiales")

p = re.compile("\w+ \w+/\d+")


# 3 sources de données
#   - voie.geojson : base de données de référence
#   - noms_voies_actuelles_paris.json : contient des renseignements historiques
#   - troncons_voies.geojson : découpage des voies en tronçons
# master_dict maintient des pointeurs permettant d'accéder à ces trois sources

master_dict = dict()

# création de master_dict à partir des données de voie.geojson

for index, record in enumerate(voies):
    l_longmin = record["properties"]["l_longmin"]
    # on élimine les voies non nommées (ex: 'voie fj/20' )
    if is_matching(normalize(l_longmin), p): continue
    n_sq_vo = record["properties"]["n_sq_vo"]
    c_voie_vp = record["properties"]["c_voie_vp"]
    k = normalize(l_longmin).replace(" ","")
    master_dict[k] = {  "index_voie_geojson" : index, 
                        "n_sq_vo" : n_sq_vo,
                        "c_voie_vp" : c_voie_vp,
                        "l_longmin" : l_longmin
                     }
print("\t", len(master_dict), "entrées après élimination des voies de type 'fj/20'")


print("# Lecture de 'noms_voies_actuelles_paris.geojson'")
with open("data/noms_voies_actuelles_paris.json", mode="r", encoding="utf8") as f:
    noms_voies_actuelles_paris = json.load(f)
print("\t", len(noms_voies_actuelles_paris), "entrées dans dans les données initiales")


# clés ambigues
# ( clé de "noms_voies_actuelles_paris.json", clé de "voie.geojson", choix manuel)
# sauf typo, le choix est de garder "noms_voies_actuelles_paris.json" comme référence (choix 2)
# choix 1 : on crée une nouvelle clé dans master_dict

equivalences = [
("placemarcellehenry", "passerellemarcellehenry", 2),
("ruemondonville", "ruemondoville", 1),
("ruedelphineseyrig", "ruedeplhineseyrig", 1),
("alleedesjustesdefrance", "alleedesjustesparmilesnations", 2),
("placeduvingtdeuxnovembre1943", "placedu22novembre1943", 2),
("petitpontcardinallustiger", "pontpetitpontcardinallustiger", 2),
("esplanadeduneufnovembre1989", "esplanadedu9novembre1989", 2),
("ruehuygens", "ruehuyghens", 2),
("ruemagenta", "ruedemagenta", 2),
("passagehypatied'alexandrie", "passagehypathied'alexandrie", 2),
("ruedugeneralalaindeboissieu", "ruedugeneraldeboissieu", 2),
("placeemmanuellevinas", "placeemanuellevinas", 1),
("impassedugue", "passagedugue", 2),
("alleeduprofesseurjeanbernard", "alleeprofesseurjeanbernard", 2),
("avenuedugeneralmargueritte", "avenuedugeneralmarguerite", 1),
("rueducardinalmercier", "ruecardinalmercier", 2),
]


# recherche des enregistrements de "noms_voies_actuelles_paris.json"
# non trouvés dans "voie.geojson"

master_dict_keys = master_dict.keys()
keys_not_found = []
for index, record in enumerate(noms_voies_actuelles_paris):
    libelle_voie = record["fields"]["libelle_voie"]
    # on élimine les voies non nommées (ex: 'voie fj/20' )
    if is_matching(normalize(libelle_voie), p): continue
    k = normalize(libelle_voie).replace(" ","")
    if k not in master_dict_keys:
        keys_not_found.append((k, index))
        continue
    master_dict[k]["index_noms_voies_actuelles_paris_json"] = index

# for key in keys_not_found:
#     print(key)


# traitement manuel

# cas 1 : la clé porte une dénomination différente dans noms_voies_actuelles_paris.json
# on conserve la clé de voie.geojson et on insère l'index de noms_voies_actuelles_paris.json

cas1 = {
"passerellemarcellehenry" : ('placemarcellehenry', 24), 
"alleedesjustesparmilesnations" : ('alleedesjustesdefrance', 3611), 
"placedu22novembre1943" : ('placeduvingtdeuxnovembre1943', 3658), 
"pontpetitpontcardinallustiger" : ('petitpontcardinallustiger', 3724), 
"esplanadedu9novembre1989" : ('esplanadeduneufnovembre1989', 3748), 
"ruehuyghens" : ('ruehuygens', 3786), 
"ruedemagenta" : ('ruemagenta', 3943), 
"passagehypathied'alexandrie" : ("passagehypatied'alexandrie", 4042), 
"ruedugeneraldeboissieu" : ('ruedugeneralalaindeboissieu', 4805), 
"passagedugue" : ('impassedugue', 5277), 
"alleeprofesseurjeanbernard" : ('alleeduprofesseurjeanbernard', 5586), 
"ruecardinalmercier" : ('rueducardinalmercier', 5963)
}

for k, v in cas1.items():
    master_dict[k]["index_noms_voies_actuelles_paris_json"] = v[1]

# cas 2 : la dénomination correcte se trouve dans noms_voies_actuelles_paris.json
# on crée une nouvelle clé, on insere le libelle de la voie et l'index
# on détruit l'ancienne clé

cas2 = {
"ruemondoville" : ('ruemondonville', 212),
"ruedeplhineseyrig" : ('ruedelphineseyrig', 749),
"placeemanuellevinas" : ('placeemmanuellevinas', 5256),
"avenuedugeneralmarguerite" : ('avenuedugeneralmargueritte', 5703),
}

for k, v in cas2.items():
    # on remplace le nom
    record = master_dict[k]
    record["l_longmin"] = noms_voies_actuelles_paris[v[1]]["fields"]["libelle_voie"]
    # nouvelle clé
    new_key = v[0]
    master_dict[new_key] = record
    # on insere l'index
    master_dict[new_key]["index_noms_voies_actuelles_paris_json"] = v[1]
    # on détruit l'ancienne clé
    del master_dict[k]

# cas 3 : les voies sont privées ou en dehors de Paris ou autre cas
# on ne fait rien

# ('placemadeleinedanielou', 87)
# ('avenuemoliere', 122)
# ('allee claudecahunmarcelmoore', 133)
# ('quaidumarcheneuf', 136)
# ('avenuedeparis', 439)
# ('impassevoltaire', 546)
# ('alleejeansablon', 550)
# ('boulevardanatolefrance', 571)
# ('parvisdesdeuxcentsoixanteenfants', 816)
# ('alleedubeaupassage', 885)
# ('carrefourdesancienscombattants', 1259)
# ('esplanadedesinvalides', 1334)
# ('ruedumarechalleclerc', 1447)
# ('placedesmartyrsdelaresistancedelaportedesevres', 1696)
# ('promenadeclairelacombe', 1697)
# ('placepierreemmanuel', 1872)
# ('squaremarcelrajman', 2109)
# ('villademontmorency', 2182)
# ('esplanaderogerjosephboscovich', 2322)
# ('villadesternes', 2370)
# ('routebosquetmortemart', 2545)
# ('portedulouvre', 2570)
# ('avenuedespreaux', 2992)
# ('boulevardducommandantcharcot', 3162)
# ('boulevardhippolytemarques', 3255)
# ('grandbalcon', 3584)
# ('placemariacallas', 3646)
# ('alleesoniarykiel', 3752)
# ('impassecorneille', 4067)
# ('portedesprinces', 4311)
# ('impasseracine', 4360)
# ('esplanadejosephwresinski', 4584)
# ("placedel'hoteldeville", 4709)
# ('alleemariacallas', 5241)
# ('avenuedugeneralmargueritte', 5703)
# ('rueauboin', 5732)
# ('buttemortemart', 5941)
# ('villamulhouse', 5942)
# ('balconsainteustache', 6327)


# recherche de la liste des troncons associés à une voie

with open("data/troncon_voie.geojson", mode="r", encoding="utf8") as f:
    troncons = json.load(f)["features"]
print(type(troncons))
print(troncons[:5])

d = defaultdict(list)
for index, t in enumerate(troncons):
    n_sq_vo = t["properties"]["n_sq_vo"]
    d[n_sq_vo].append(index)

# insertion de la liste dans master_dict

for k, v in master_dict.items():
    n_sq_vo = v["n_sq_vo"]
    master_dict[k]["troncons"] = d[n_sq_vo]

print("# Ecriture de 'out/odp_masterdict.json'")
with open("out/odp_masterdict.json", mode="w", encoding="utf8") as f:
    json.dump(master_dict, f)




