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


def get_paged_data(query):
    last_response = get_data(query)
    while last_response["data"]["fields"]:
        yield last_response
        query["variables"]["cursor"] = last_response["data"]["fields"][-1]["cursor"]
        last_response = get_data(query)
