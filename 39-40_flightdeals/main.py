#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from datetime import datetime, timedelta
import time
from notification_manager import NotificationManager

dataman=DataManager()
flightsearcher=FlightSearch()
sendmessage=NotificationManager

# Set your origin airport
ORIGIN_CITY_IATA = "PRG"

sheet_data=dataman.get_city_names()
print(sheet_data)
for line in sheet_data:
    line["iataCode"]=flightsearcher.get_destination_code(line["city"])
print(sheet_data)

dataman.cities=sheet_data
dataman.fill_IATA()

# ==================== Search for Flights ====================

tomorrow = datetime.now() + timedelta(days=1)
one_month_from_today = datetime.now() + timedelta(days=(30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flightsearcher.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=one_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # ==================== Send alert t o SMS ====================
    if destination["Lowest Price"] > cheapest_flight.price:

        orig=ORIGIN_CITY_IATA
        dest=destination["iataCode"]
        sendmessage.send_message(message_details=f"New cheapest flight! from: {orig} to:{dest} FROM:{cheapest_flight.out_date} TO:{cheapest_flight.return_date} price: {cheapest_flight.price} €")


    # Slowing down requests to avoid rate limit



    time.sleep(3)





