#!/usr/bin/python3

"""
    search.py

    MediaWiki API Demos
    Demo of `Search` module: Search for a text or title

    MIT License
"""

import requests
import json

S = requests.Session()

URL = "https://fr.wikipedia.org/w/api.php"

SEARCHPAGE = "Nelson Mandela"

PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": SEARCHPAGE
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

with open("out.json", mode='w') as f:
    json.dump(DATA, f)


if DATA['query']['search'][0]['title'] == SEARCHPAGE:
    print("Your search page '" + SEARCHPAGE + "' exists on French Wikipedia")