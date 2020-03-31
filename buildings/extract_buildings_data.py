import json

with open("liste-des-immeubles-proteges-au-titre-des-monuments-historiques.json", mode="r", encoding="utf8") as f:
    records = json.load(f)

stat = []
insee = []
scle = []
ref = []
adrs = []
coordonnees_ban = []
ppro = []
hist = []
wadrs = []
tico = []
pop_date = []

fields_of_interest = { "stat" : stat,
"insee" : insee,
"scle" : scle,
"ref" : ref,
"adrs" : adrs,
"coordonnees_ban" : coordonnees_ban,
"ppro" : ppro,
"hist" : hist,
"wadrs" : wadrs,
"tico" : tico,
"pop_date" : pop_date,

}

# get missing fields in records

print("Exploring JSON structure...")
for record in records:

    for field in fields_of_interest:
        try:
            if record["fields"][field]:
                pass
        except:
            fields_of_interest[field].append(record["recordid"])


for field in fields_of_interest:
    print(field, " : ", len(fields_of_interest[field]), "are missing")




