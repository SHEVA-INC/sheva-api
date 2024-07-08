import requests
from transliterate import translit

REGIONS = {}
CITIES = {}
WAREHOUSES = {}

url = "https://api.novaposhta.ua/v2.0/json/"

def get_regions():
    payload = {
        "apiKey": "89256a3aacc743a054931497a53d7c24",
        "modelName": "AddressGeneral",
        "calledMethod": "getAreas",
    }
    response = requests.post(url, json=payload)
    data = response.json()
    areas = data["data"]

    for area in areas:
        description = area['Description']
        transliterated_text = translit(description, 'uk', reversed=True)
        REGIONS.update({transliterated_text: {'ref': area['Ref'], 'description': description}})

    return REGIONS

def get_cities_by_region(region_ref):
    payload = {
        "apiKey": "89256a3aacc743a054931497a53d7c24",
        "modelName": "AddressGeneral",
        "calledMethod": "getCities",
        "methodProperties": {
            "AreaRef": region_ref
        }
    }
    response = requests.post(url, json=payload)
    data = response.json()
    cities = data["data"]

    for city in cities:
        description = city['Description']
        transliterated_text = translit(description, 'uk', reversed=True)
        CITIES.update({transliterated_text: {'ref': city['Ref'], 'description': description}})

    return CITIES

def get_warehouses_by_city(city_ref):
    payload = {
        "apiKey": "89256a3aacc743a054931497a53d7c24",
        "modelName": "AddressGeneral",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityRef": city_ref
        }
    }
    response = requests.post(url, json=payload)
    data = response.json()
    warehouses = data["data"]

    for warehouse in warehouses:
        description = warehouse['Description']
        transliterated_text = translit(description, 'uk', reversed=True)
        WAREHOUSES.update({transliterated_text: description})

    return WAREHOUSES

# # Пример использования:
# regions = get_regions()
# print("Regions:", regions)

# region_ref = '71508134-9b87-11de-822f-000c2965ae0e'
# cities = get_cities_by_region(region_ref)
# print("Cities:", cities)
#
city_ref = 'f9687167-d4f7-11e2-874c-d4ae527baec3'
warehouses = get_warehouses_by_city(city_ref)
print("Warehouses:", warehouses)
