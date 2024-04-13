import requests
from transliterate import translit

REGIONS = {}
CITIES = {}
WAREHOUSES = {}

url = "https://api.novaposhta.ua/v2.0/json/"


def get_regions():
    payload = {
        "apiKey": "89256a3aacc743a054931497a53d7c24",
        "modelName": "Address",
        "calledMethod": "getAreas",
    }
    response = requests.post(url, json=payload)
    data = response.json()
    areas = data["data"]

    for area in areas:
        description = area['Description']
        transliterated_text = translit(description, 'uk', reversed=True)
        REGIONS.update({transliterated_text: description})

    return REGIONS


payload = {
    "apiKey": "89256a3aacc743a054931497a53d7c24",
    "modelName": "Address",
    "calledMethod": "getCities",
    "methodProperties": {
        "AreaRef": "your_area_ref"
    }
}
response = requests.post(url, json=payload)
data = response.json()
cities = data["data"]
print(cities)
