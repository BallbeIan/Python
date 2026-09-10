import os
import requests
import argparse
from dotenv import load_dotenv, find_dotenv

load_dotenv(("api.env"))

def get_flight_information(number):
    "Retreives the API information from the .env folder, the sends the HTTP GET request with the necessary"
    "information to retreive all data from the requested flight."
    api = os.getenv("aviation_api")
    url = os.getenv("aviation_url")
    params = {
            "access_key" : api,
            "flight_iata" : number
            }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        flight_info = response.json()
        data = flight_info.get("data", [])
        flight_information = data[0]
        departure = flight_information.get("departure", {})
        arrival = flight_information.get("arrival", {})
        airline = flight_information.get("airline", {})
        flight = flight_information.get("flight", {})
        aircraft = flight_information.get("aircraft", {})
        live = flight_information.get("live", {})

        if data:
            print(f"+", "="*50, "+")
            print(f"| Departure and Arrival")
            print(f"| Date: ", departure.get("scheduled", "Not available"))
            print(f"| Arrival Date & Time: ", arrival.get("scheduled", "Not Available"))
            print(f"+", "-"*50, "+")
            print(f"| Airline Information")
            print(f"| Airline: ", airline.get("name", "Not available"))
            print(f"+", "-"*50, "+")
            print(f"| Aircraft Information")
            print(f"| Aircraft Registration: ", aircraft.get("registration", "Not available"))
            print(f"+", "="*50, "+")
        else:
            print("No flight data found.")
    else:
        print(f"Request failed {response.status_code}")

#============================================================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
    "Airplane to track"
    )
    parser.add_argument("-f", "--flight", required=True, type=str)
    args=parser.parse_args()

    flight = args.flight

    get_flight_information(flight)
