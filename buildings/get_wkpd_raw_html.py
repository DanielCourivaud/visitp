# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Récupération des données Wikipedia : "Bâtiments remarquables et lieux de mémoire" 

# %%
import requests
from bs4 import BeautifulSoup
from itertools import takewhile


# %%
url = "https://fr.wikipedia.org/wiki/Rue_de_Bagnolet"


# %%
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")


# %%
h2s = soup.find_all("h2")
for h2 in h2s:
    print(h2.text)
    print()
    data = takewhile(lambda t: t.name == 'ul',
                         h2.find_next_siblings(text=False))
    for d in data:
        print(d)
        print()

