# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json



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
BASE_URL = "https://fr.wikipedia.org/wiki/"

ARRS = [ i+1 for i in range(20)]
# ARRS = ARRS[13:14]



def get_wkpd_html(url):
    url = BASE_URL + url
    r = requests.get(url)
    return r.text



def get_streets(arr, html):
    soup = BeautifulSoup(html, "html.parser")

    # get all links
    links = soup.find_all('a')

    results = []

    for link in links:
        # print(link)
        attrs = link.attrs
        if "href" not in attrs.keys() : continue

        if ":" in attrs["href"] : continue

        if '/wiki/' not in attrs["href"] : continue
        if 'Portail:' in attrs["href"] : continue
        if 'arrondissement' in attrs["href"] : continue

        if "title" in attrs.keys() :
            if attrs["title"] == "Paris" : continue
            if attrs["title"] == "France" : continue
            if attrs["title"] == "Voie sans nom de Paris": continue
            if attrs["title"] == "Liste des anciens noms de voies de Paris" : continue
            if attrs["title"] == "Liste des voies de Paris" : continue
            if attrs["title"] == "Réseau viaire de Paris" : continue
            if attrs["title"] == "OpenStreetMap" : continue
            if attrs["title"] == "Bing Cartes" : continue
            if attrs["title"] == "Keyhole Markup Language" : continue

            # arr 12
            if attrs["title"] == "Jean Verdier (préfet)" : continue
            if attrs["title"] == "1970" : continue
            if attrs["title"] == "1972" : continue
            if attrs["title"] == "1991" : continue
            if attrs["title"] == "1997" : continue
            if attrs["title"] == "Jean Tiberi" : continue
            if attrs["title"] == "Liste des maires de Paris" : continue
            if attrs["title"] == "International Standard Book Number" : continue
            if attrs["title"] == "Alfred Fierro" : continue
            if attrs["title"] == "1999" : continue
            if attrs["title"] == "Liste des places de Paris" : continue
            if attrs["title"] == "Sentiers de Paris" : continue
            if attrs["title"] == "Ruelles de Paris" : continue

            # arr 20
            if attrs["title"] == "Belleville (Seine)" : continue
            if attrs["title"] == "Charonne (Seine)" : continue
            if attrs["title"] == "Ménilmontant (quartier parisien)" : continue

            if "Modèle:" in attrs["title"] : continue
            if "Catégorie:" in attrs["title"] : continue
            

        if "class" in attrs.keys() :
            # print(attrs["class"])
            if "image" in attrs["class"] : continue
            if "internal" in attrs["class"] : continue    

        # print("!")
        # results.append(str(link))
        results.append( (arr, attrs["title"], attrs["href"]) )

    return results



def export(obj):
    with open("out.json", mode='w', encoding="utf8") as f:
        json.dump(obj, f)



def main():
    for arr in ARRS:
        print(arr)
        html = get_wkpd_html(STREETS_BY_ARR[arr])
        links = get_streets(arr, html)
        # print(type(links))
        # print("---")
        # print(len(links))
        # print(links)

        with open("out/list_of_streets.txt", mode='a', encoding="utf8") as f:
            for l in links:
                # s = "{0:<10} {1:<50} {2} \n".format(str(l[0]), l[1], l[2])
                s = "{0} # {1} # {2}\n".format(str(l[0]), l[1], l[2])
                f.write(s)
               

        # export(links)



main()




