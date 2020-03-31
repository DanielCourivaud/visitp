"""
extrait les différents types de voies à partir du JSON Open Data Paris
"""


import json
import re

JSONFILE = "data/noms_voies_actuelles_paris.json"

NO_NAME_PATTERN = re.compile("\w+/\d+")

with open(JSONFILE, mode="r", encoding="utf8") as f:
    streets = json.load(f)

print(len(streets))

def has_a_name(street):
    return not NO_NAME_PATTERN.match(street["fields"]["nom_de_voie"])


types_de_voies = set()

for street in streets:
    try:
        types_de_voies.add(street["fields"]["type_de_voie"])
    except:
        pass


with open("out/types_de_voies.txt", mode="w", encoding="utf8") as f:
    json.dump(sorted(list(types_de_voies)), f, ensure_ascii=False)






