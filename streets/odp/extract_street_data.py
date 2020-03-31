import json
from statistics import mean


# Lecture des sources de données ODP

with open("data/voie.geojson", mode="r", encoding="utf8") as f:
    voies_geojson = json.load(f)

with open("data/noms_voies_actuelles_paris.json", mode="r", encoding="utf8") as f:
    noms_voies_actuelles_paris = json.load(f)

with open("data/troncon_voie.geojson", mode="r", encoding="utf8") as f:
    troncons = json.load(f)["features"]

# Lecture du master dict
# contient des pointeurs vers les sources de données ODP

with open("out/odp_masterdict.json", mode="r", encoding="utf8") as f:
    master_dict = json.load(f)


# Troncon de voie

class Troncon():

    def __init__(self, id): 
        self.id = id
        self.data = troncons[id]
        self.nsqvo = self.data["properties"]["n_sq_vo"]
        self.length = self.data["properties"]["length"]

        self.dg = self.data["properties"]["n_voieaddg"]
        self.dd = self.data["properties"]["n_voieaddd"]
        self.fd = self.data["properties"]["n_voieadfd"]
        self.fg = self.data["properties"]["n_voieadfg"]

        self.left_side = [self.dg, self.fg]
        self.right_side = [self.dd, self.fd]

        self.limites = (self.left_side, self.right_side)

        self.geometry = self.data["geometry"]


    def is_left_valid(self):
         return  self.left_side != [0, 0]


    def is_right_valid(self):
         return  self.right_side != [0, 0]
    

    def is_not_valid(self):
        return  not ( self.is_left_valid() or self.is_right_valid() )
              

    def __str__(self):
        return str(self.limites)

# Rue

class Street():

    def __init__(self, street_key):

        self.nom = master_dict[street_key]["l_longmin"]
        self.nsqvo = master_dict[street_key]["n_sq_vo"]
        self.cvoievp = master_dict[street_key]["c_voie_vp"]
        self.index_voie = master_dict[street_key]["index_voie_geojson"]
        self.index_nom = master_dict[street_key]["index_noms_voies_actuelles_paris_json"]
        self.historique = noms_voies_actuelles_paris[self.index_nom]["fields"]["historique"]
        self.detail = noms_voies_actuelles_paris[self.index_nom]["fields"]["detail"]
        self.quartier = noms_voies_actuelles_paris[self.index_nom]["fields"]["quartier"]
        self.longueur = noms_voies_actuelles_paris[self.index_nom]["fields"]["long"]
        self.largeur = noms_voies_actuelles_paris[self.index_nom]["fields"]["largeur"]
        self.debut = noms_voies_actuelles_paris[self.index_nom]["fields"]["debut"]
        self.fin = noms_voies_actuelles_paris[self.index_nom]["fields"]["fin"]
        
        self.troncons = list()
        for t_id in master_dict[street_key]["troncons"]:
            t = Troncon(t_id)
            if t.is_not_valid(): continue
            self.troncons.append(t)
        self.troncons = self.order_troncons()
        self.n_troncons = len(self.troncons)

        
    def order_troncons(self):
        l = sorted(self.troncons, key = lambda t:max(t.left_side))
        not_left_valids = [ t for t in self.troncons if not t.is_left_valid() ]

        for t in not_left_valids:
            m = max(t.right_side)
            print(t, m)


        return l

        

    def __str__(self):
        return self.nom + \
                str(self.nsqvo) + "\n" + \
                self.cvoievp + "\n" + \
                str(self.index_voie) + "\n" + \
                str(self.index_nom) + "\n" + \
                str(self.troncons) + "\n" + \
                self.historique + "\n" + \
                self.detail + "\n" + \
                self.quartier + "\n" + \
                str(self.longueur) + "\n" + \
                str(self.largeur) + "\n" + \
                self.debut + "\n" + \
                self.fin


def main():
    street_key = "ruedecharonne"
    s = Street(street_key)
    print(s)
    for t in s.troncons:
        if t.is_right_valid(): 
            print(t.limites)


if __name__ == "__main__":
    main()








