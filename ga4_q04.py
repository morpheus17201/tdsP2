# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "bs4",
# ]
# ///


import requests
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
import os

# Constants (replace with actual values)
BBC_WEATHER_KEY = os.environ["BBC_WEATHER_KEY"]
# CITY = "Kuala Lumpur"
BASE_URL = "https://api.bbc.com/weather"
LOCATOR_URL = f"{BASE_URL}/locator"


# Step 1: Get Location ID for Kuala Lumpur
def get_location_id(city, api_key):
    params = {
        "q": city,
        "apiKey": api_key,
        "locale": "en",  # Example locale
    }

    location_url = "https://locator-service.api.bbci.co.uk/locations?" + urlencode(
        {
            "api_key": BBC_WEATHER_KEY,
            "s": city,
            "stack": "aws",
            "locale": "en",
            "filter": "international",
            "place-types": "settlement,airport,district",
            "order": "importance",
            "a": "true",
            "format": "json",
        }
    )

    # response = requests.get(LOCATOR_URL, params=params)
    response = requests.get(location_url).json()
    return response["response"]["results"]["results"][0]["id"]


def get_weather_data(location_id):
    # url = "https://www.bbc.com/weather/" + location_id
    url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{location_id}"
    response = requests.get(url)
    return response


# Step 3: Extract relevant data and create JSON output
def extract_weather_data(output):

    data = json.loads(output.text)
    output_dict = {}
    for forecast in data["forecasts"]:
        date = forecast["summary"]["report"]["localDate"]
        desc = forecast["summary"]["report"]["enhancedWeatherDescription"]
        # print(f"{date=}, {desc=}")
        output_dict[date] = desc

    # print(output_dict)

    return output_dict


# Main workflow
def get_bbc_weather(CITY):
    location_id = get_location_id(CITY, BBC_WEATHER_KEY)
    print(f"{location_id=}")
    if location_id:
        weather_data = get_weather_data(location_id)
        if weather_data:
            weather_dict = extract_weather_data(weather_data)
            # print("{")
            # json = ",\n".join([f'"{k}": "{v}"' for k, v in weather_dict.items()])
            # print(json)
            # print("}")

    return json.dumps(weather_dict)


if __name__ == "__main__":
    print(get_bbc_weather("Kuala Lumpur"))
