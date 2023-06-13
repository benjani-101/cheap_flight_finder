from datetime import datetime

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, data):
        self.fly_from_iata = data['flyFrom']
        self.fly_to_iata = data['flyTo']
        self.city_from = data['cityFrom']
        self.city_to = data['cityTo']
        self.departure_time = datetime.fromtimestamp(data['dTime'])
        self.arrival_time = datetime.fromtimestamp(data['aTime'])
        for flight in data['route']:
            if flight['flyTo'] == self.fly_from_iata:
                self.return_departure_time = datetime.fromtimestamp(flight['dTime'])
                self.return_arrival_time = datetime.fromtimestamp(flight['aTime'])
                break
        self.price = data['price']
        self.link = data['deep_link']
