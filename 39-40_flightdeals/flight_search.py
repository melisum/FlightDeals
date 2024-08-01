import os
import datetime
import requests
TOKEN_ENDPOINT="https://test.api.amadeus.com/v1/security/oauth2/token"
Amadeus_API_KEY = os.getenv("Amadeus_API_KEY")
Amadeus_API_Secret = os.getenv("Amadeus_API_Secret")
amadeus_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"

token_type= "Bearer"
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._token=self.get_token()

    def get_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': Amadeus_API_KEY,
            'client_secret': Amadeus_API_Secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        return response.json()['access_token']


    def get_destination_code(self, city_name):
        # Return "TESTING" for now to make sure Sheety is working. Get TEQUILA API data later.
        url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        header= {
            "Authorization": f"Bearer {self._token}"
        }
        parameters={
            "keyword":city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=url, headers=header, params=parameters)

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """
        Searches for flight options between two cities on specified departure and return dates
        using the Amadeus API.
        Parameters:
            origin_city_code (str): The IATA code of the departure city.
            destination_city_code (str): The IATA code of the destination city.
            from_time (datetime): The departure date.
            to_time (datetime): The return date.
        Returns:
            dict or None: A dictionary containing flight offer data if the query is successful; None
            if there is an error.
        The function constructs a query with the flight search parameters and sends a GET request to
        the API. It handles the response, checking the status code and parsing the JSON data if the
        request is successful. If the response status code is not 200, it logs an error message and
        provides a link to the API documentation for status code details.
        """

        # print(f"Using this token to check_flights() {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "EUR",
            "max": "10",
        }

        response = requests.get(
            url=amadeus_endpoint,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()

#params example:
#?origin=PAR&maxPrice=200' \-H 'Authorization: Bearer ABCDEFGH12345'

#example
#{
#     "data": [
#         {
#             "type": "flight-destination",
#             "origin": "PAR",
#             "destination": "CAS",
#             "departureDate": "2022-09-06",
#             "returnDate": "2022-09-11",
#             "price": {
#                 "total": "161.90"
#             }
#         },
#         {
#             "type": "flight-destination",
#             "origin": "PAR",
#             "destination": "AYT",
#             "departureDate": "2022-10-16",
#             "returnDate": "2022-10-31",
#             "price": {
#                 "total": "181.50"
#             }
#         }
#     ]
# }