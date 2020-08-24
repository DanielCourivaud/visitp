from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json


ARRS = [ str(i+1)+"e" for i in range(20)]
ARRS[0] += "r"
FMT_STRING = "Liste_des_monuments_historiques_du_{0}_arrondissement_de_Paris"
BUILDINGS_BY_ARR = { (i+1):FMT_STRING.format(ARRS[i]) for i in range(20)}

BASE_URL = "https://fr.wikipedia.org/wiki/"


def get_wkpd_html(url):
    url = BASE_URL + url
    r = requests.get(url)
    return r.text


def extract_building_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # find tables
    tables = soup.findAll('table', attrs={"class":"wikitable sortable"})

    # get the first one
    table = tables[0]

    # find all <tr>
    trs = table.findAll(['tr'])

    monuments_list = []

    for tr in trs:
        tds = tr.findAll(['td'])

        if not tds: continue

        d = dict()

        # print(tds)
        monument, adresse, coords, notice, protection, date, illustration = tds

        # print(monument)
        name = monument.text.strip()
        try:
            href = monument.find('a').attrs['href']
        except:
            href = None
        # print(name)
        # print(href)

        adresse = adresse.text.strip()
        # print(adresse)

        try:
            coords = coords.find('a').attrs
            coords = (coords['data-lat'], coords['data-lon'])
        except:
            coords = None
        # print(coords)

        notice = notice.find('a').attrs['href']
        # print(notice)
        key = notice.split('//')[-1]
        # print(key)

        protection = protection.text.strip()
        # print(protection)

        date = date.text.strip()
        # print(date)

        illustration = illustration.find('a').attrs['href']
        # print(illustration)

        d["key"] = key
        d["name"] = name
        d["adresse"] = adresse
        d["coords"] = coords
        d["href"] = href
        d["notice"] = notice
        d["protection"] = protection
        d["date"] = date
        d["illustration"] = illustration

        monuments_list.append(d)

    return monuments_list


def main():
    all = []
    for arr in range(1, 21):
        # print(BUILDINGS_BY_ARR[arr])
        html = get_wkpd_html(BUILDINGS_BY_ARR[arr])
        monuments_by_arr = extract_building_data(html)
        # print(monuments_by_arr[0])
        all.extend(monuments_by_arr)
    # print(len(all))

    with open("mh_wkpd.json", mode='w', encoding="utf8") as f:
        json.dump(all, f)


main()