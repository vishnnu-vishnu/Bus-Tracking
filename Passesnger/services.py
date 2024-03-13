# services/services.py

import requests



def get_coordinates(place_name):
    # your actual API key for https://locationiq.com/
    api_key = 'pk.3157b48fb3fb325a658d2919fc0ca80c'
    base_url = f'https://us1.locationiq.com/v1/search?q={place_name}&format=json'
    params = {

        'key': api_key,
    }

    response = requests.get(base_url,params=params)
    data = response.json()

    location = data[0]
    if response.status_code == 200:
        location=data[-1]
        return location['lat'], location['lon']
    else:
        return None

def get_Bus_stations(lat, lng):
    # your actual API key for https://locationiq.com/
    api_key = 'pk.3157b48fb3fb325a658d2919fc0ca80c'

    base_url = "https://us1.locationiq.com/v1/nearby"
    params = {
        'key': api_key,
        'lat': lat,
        'lon': lng,
        'tag': 'bus_station',
        'radius': 5000,
        'format': 'json'
    }

    response = requests.get(base_url,params=params)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None
    






def get_fuel_stations(lat, lng):
    api_key = 'pk.3157b48fb3fb325a658d2919fc0ca80c'
    base_url = "https://us1.locationiq.com/v1/nearby"
    params = {
        'key': api_key,
        'lat': lat,
        'lon': lng,
        'tag': 'fuel',
        'radius': 2000,
        'format': 'json'
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None
def get_workshops(lat, lng):
    api_key = 'pk.3157b48fb3fb325a658d2919fc0ca80c'
    base_url = "https://us1.locationiq.com/v1/nearby"
    params = {
        'key': api_key,
        'lat': lat,
        'lon': lng,
        'tag': 'shop:car_repair',
        'radius': 10000,
        'format': 'json'
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None







