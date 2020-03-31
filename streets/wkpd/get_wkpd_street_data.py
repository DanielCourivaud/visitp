"""
Extrait les batiments remarquables de la page Wikipedia d'une rue
"""


from bs4 import BeautifulSoup
import requests

BASE_URL = "https://fr.wikipedia.org/"

def get_street_info(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "infobox_v2"})
    x = table.findAll("th", {"scope" : "row"})
    print(x)

def get_street_html(street_url="wiki/Rue_de_Charonne"):
    url = BASE_URL + street_url
    r = requests.get(url)
    return r.text

def main():
    street_url="wiki/Rue_de_Charonne"
    html_data = get_street_html(street_url)
    get_street_info(html_data)

if __name__ == "__main__":
    main()


