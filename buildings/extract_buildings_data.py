import json

with open("liste-des-immeubles-proteges-au-titre-des-monuments-historiques.json", mode="r", encoding="utf8") as f:
    records = json.load(f)

print(len(records), "buildings in the database")

fields_of_interest = { "stat" : [],
"insee" : [],
"scle" : [],
"ref" : [],
"adrs" : [],
"coordonnees_ban" : [],
"ppro" : [],
"hist" : [],
"wadrs" : [],
"tico" : [],
"pop_date" : [],
"geometry" : []

}

# get missing fields in records

print("Exploring JSON structure...")
for record in records:

    for field in fields_of_interest.keys():
        if field == "geometry": continue
        try:
            if record["fields"][field]:
                pass
        except:
            fields_of_interest[field].append(record["recordid"])

    try:
        if record["geometry"]:
            # print("found")
            pass
    except:
        fields_of_interest["geometry"].append(record["recordid"])


for field in fields_of_interest.keys():
    print("\t", field, " : ", len(fields_of_interest[field]), "are missing")



