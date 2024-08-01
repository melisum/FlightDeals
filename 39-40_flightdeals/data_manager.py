import requests
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_url = "https://api.sheety.co/165b8ba46b7a0bfc511be91b3d58a148/flightDeals/prices"
        self.sheetypasskey = os.getenv("sheetypasskey")
        self.header = {
            "Authorization": f"Basic {self.sheetypasskey}"
        }
        self.requests=requests
        self.cities={}
    def get_city_names(self):

        getdata=self.requests.get(url=self.sheety_url, headers=self.header)
        print(getdata.text)
        data=getdata.json()
        self.cities=data["prices"]
        return self.cities

    def fill_IATA(self):
        for city in self.cities:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response=self.requests.put(url=f"{self.sheety_url}/{city['id']}", json=new_data, headers=self.header)
        print(response.text)
