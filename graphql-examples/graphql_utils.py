import os
import requests

APIM_KEY = os.environ.get("APIM_KEY")
BASE_URL = "https://api.agrimetrics.co.uk/graphql"


def get_data(query):
    response = requests.post(
        url=BASE_URL,
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "ocp-apim-subscription-key": APIM_KEY,
        },
        json=query,
    )

    response.raise_for_status()
    return response.json()


def get_paged_field_data(query):
    while True:
        last_response = get_data(query)
        
        field_data = last_response["data"]["fields"]
        yield field_data
        
        if not field_data:
            break

        last_cursor = field_data[-1]["cursor"]

        if last_cursor is None:
            break

        query["variables"]["cursor"] = last_cursor


def get_paged_rainfall_data(query):
    while True:
        last_response = get_data(query)
        
        weather_observations = last_response["data"]["node"]["weatherObservations"]
        yield weather_observations["rainfallTotalDaily"]

        if not weather_observations:
            break

        last_cursor = weather_observations["cursor"]

        if last_cursor is None:
            break

        query["variables"]["cursor"] = last_cursor


