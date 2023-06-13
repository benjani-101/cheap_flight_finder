from datetime import datetime, timedelta
import os
import requests

flight_search_api_key = os.environ.get('flight_search_api_key')

flight_search_endpoint = "https://api.tequila.kiwi.com/"

#This class is responsible for talking to the Flight Search API.
class FlightSearch:
    def __init__(self):
        self.endpoint = flight_search_endpoint
        self.headers = {
            "apikey": flight_search_api_key,
        }

    def search_city_data(self, city):
        params = {
            'term': city.lower(),
            'locale': 'en-US',
            'location_types': 'city',
        }
        response = requests.get(url=f"{self.endpoint}locations/query", params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_flights(self, iata_code_from, iata_code_to, price_to):
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        six_months_date = datetime.now().replace(month=datetime.now().month + 6).strftime("%d/%m/%Y")
        params = {
            'fly_from': iata_code_from,
            'fly_to': iata_code_to,
            'date_from': tomorrow,
            'date_to': six_months_date,
            'nights_in_dst_from': 3,
            'nights_in_dst_to': 14,
            'ret_from_diff_city': False,
            'ret_to_diff_city': False,
            'price_to': price_to,
            'max_stopovers': 0
        }
        response = requests.get(url=f"{self.endpoint}search", params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()



