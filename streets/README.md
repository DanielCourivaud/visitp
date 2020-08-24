# Source des données

## APUR

http://opendata.apur.org/

## Open Data Paris

[https://opendata.paris.fr/explore/dataset/voie/information/](https://opendata.paris.fr/explore/dataset/voie/information/)
[https://opendata.paris.fr/explore/dataset/noms_voies_actuelles_paris](https://opendata.paris.fr/explore/dataset/noms_voies_actuelles_paris)
[https://opendata.paris.fr/explore/dataset/troncon_voie/](https://opendata.paris.fr/explore/dataset/troncon_voie/)

## Wikipedia

[https://fr.wikipedia.org/wiki/Liste_des_voies_du_1er_arrondissement_de_Paris](https://fr.wikipedia.org/wiki/Liste_des_voies_du_1er_arrondissement_de_Paris)
...
[https://fr.wikipedia.org/wiki/Liste_des_voies_du_20e_arrondissement_de_Paris](https://fr.wikipedia.org/wiki/Liste_des_voies_du_20e_arrondissement_de_Paris)

Le scraping Beautiful Soup est complexe à cause du manque de structuration des pages ci dessus.

Les fichiers `voies_arr_xx.txt` ont été extraits manuellement.

L'extraction se fait à partir du fichier `get_streets_from_wkpd.py`. Le fichier `data\c_streets_from_wkpd.json` est produit.





