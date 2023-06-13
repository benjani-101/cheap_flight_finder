import requests
import os

import flight_search

sheety_endpoint = os.environ.get('SHEETY_API')
sheety_auth_token = os.environ.get('SHEETY_AUTH_TOKEN')


#This class is responsible for talking to the Google Sheet.
class DataManager:
    def __init__(self):
        self.endpoint = sheety_endpoint
        self.headers = {
            "Authorization": "Bearer " + sheety_auth_token,
            "Content-Type": "application/json"
        }


    def get_data_json(self):
        response = requests.get(url=self.endpoint, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data

    def add_city(self, city, lowest_price):
        params = {
            "price": {
                "city": city.title(),
                "lowestPrice": lowest_price
            }
        }
        response = requests.post(url=self.endpoint, json=params, headers=self.headers)
        response.raise_for_status()

    def update(self, city, lowest_price):
        data = self.get_data_json()
        for row in data['prices']:
            if row['city'].lower() == city.lower():
                row_id = row['id']
                params = {
                    'price': {
                        'lowestPrice': lowest_price
                    }
                }
                response = requests.put(url=f"{self.endpoint}/{row_id}", headers=self.headers, json=params)
                response.raise_for_status()
                return print(response.json())
        self.add_city(city=city, lowest_price=lowest_price)

    def update_iata_code(self, row_id, flight_search_json):
        iata_code = flight_search_json['locations'][0]["code"]
        params = {
            'price': {
                'iataCode': iata_code
            }
        }
        response = requests.put(url=f"{self.endpoint}/{row_id}", headers=self.headers, json=params)
        response.raise_for_status()



# dm = DataManager()
# print(dm.get_data_json())
#
# # dm.update(city="Chicago", lowest_price=300)
# fs = flight_search.FlightSearch()
# dm.update_iata_codes(flight_search_obj=fs)

