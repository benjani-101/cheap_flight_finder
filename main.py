#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData
from twilio.rest import Client
import os


from_airport = 'MAN'
dm = DataManager()
fs = FlightSearch()

def update_iata():
    data_json = dm.get_data_json()
    for row in data_json['prices']:
        if row['iataCode'] == '':
            flight_search_json = fs.search_city_data(row['city'])
            dm.update_iata_code(row_id=row['id'], flight_search_json=flight_search_json)

# dm.update(city="Chicago", lowest_price=300)

def search_for_flights():
    flights = {}
    sheet_data = dm.get_data_json()
    for row in sheet_data['prices']:
        city = row['city']
        iata_codes = row['iataCode']
        max_price = row['lowestPrice']
        flight_search_json = fs.search_flights(iata_code_from=from_airport,
                                               iata_code_to=iata_codes,
                                               price_to=max_price-1)
        flight_json = flight_search_json['data']
        flights[city] = [FlightData(flight) for flight in flight_json]
        # for flight in flights[city]:
        #     print(f'to_iata: {flight.fly_to_iata}\n',
        #           f'from_iata: {flight.fly_from_iata}\n',
        #           f'price: {flight.price}\n',
        #           f'arr: {flight.arrival_time}\n',
        #           f'dep: {flight.departure_time}\n',
        #           f'return_arr: {flight.return_arrival_time}\n',
        #           f'return_dep: {flight.return_departure_time}\n',
        #           f'city_from: {flight.city_from}\n',
        #           f'city_to: {flight.city_to}\n',
        #           f'link: {flight.link}\n',)
    return flights




def sms_message(message, to_number):
    client = Client(os.environ.get('TW_ACCOUNT_SID'), os.environ.get('TW_AUTH_TOKEN'))
    message = client.messages.create(
                                  body=message,
                                  from_=os.environ.get('TW_PHONE_NUMBER'),
                                  to=to_number
                              )

    print(message.sid)
    print(message.status)

update_iata()
flights = search_for_flights()
for city in flights:
    for flight in flights[city]:
        message = f"Only €{flight.price} to fly from {flight.city_from}-{flight.fly_from_iata} " \
                  f"to {city}-{flight.fly_to_iata}, " \
                  f"from {flight.departure_time.date()} to {flight.return_departure_time.date()}"
        sms_message(message, os.environ.get('MY_NUMBER'))


