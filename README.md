# vp

## Ressources

### Techniques

[Alpage](https://alpage.huma-num.fr)
http://mapd.sig.huma-num.fr/alpage_public/flash/
[Protections patrimoniales](http://pluenligne.paris.fr/plu/sites-plu/site_statique_37/pages/page_783.html])
[Immeubles protégés au titre des Monuments Historiques](https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/information/?refine.dpt_lettre=Paris)

### Historiques

[Atlas historique de Paris](http://paris-atlas-historique.fr)
[Paristoric](https://www.paristoric.com/)
[Patrimoine de France](http://patrimoine-de-france.com/paris/)
[Paris 1850](https://paris1850.fr/)
[Archives de Paris](http://archives.paris.fr/)

### Balades

[Paris parcours](https://www.parisparcours.com/accueil)

### Applications

https://www.pavillon-arsenal.com/fr/documentation/11096-guide-paris-archi.html

### Blogs

[Paris-bise-art](https://paris-bise-art.blogspot.com/)
[Paris myope](http://parismyope.blogspot.com/)
[Les Paris DLD](https://www.lesparisdld.com/p/visites.html)
[Histoires de Paris](https://www.histoires-de-paris.fr/)
[vergue.com](http://vergue.com/)
[Parisienne Curieuse](http://anetcha-parisienne.blogspot.com/)
[Paris promeneurs](http://www.paris-promeneurs.com/)
[Des usines à Paris](http://lafabriquedeparis.blogspot.com/)
[http://www.parisapied.net](http://www.parisapied.net/)
[Autour de Paris](https://autour-de-paris.com/)
[Paris inconnu](http://www.parisinconnu.com)

### Documents

[Paris en Marches](http://50ans.apur.org/data/b4s3_home/fiche/90/08_paris_en_marches_45f4f.pdf)


# Installation

Crée le container (une seule fois)
## Mongo
```
docker run -d -p 27017:27017 --name=mongo -v ~/Documents/visitp/db:/data/db mongo
```

# Lancement
Démarre le container 
```
sudo docker start mongo
```

Supprime le container 
sudo docker rm -f mongo


Liste tous les containers présents sur la machiner
sudo docker ps -a

Liste tous les containers actifs
sudo docker ps






