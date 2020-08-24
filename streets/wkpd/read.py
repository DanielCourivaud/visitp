import json

with open("out/wkpd_streets.json") as f:
    data = json.load(f)

print(type(data))

keys = list(data.keys())

for key in keys[:10]:
    print(key, data[key])