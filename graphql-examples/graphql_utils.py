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
    while True:
        last_response = get_data(query)
        yield last_response

        if not last_response["data"]["fields"]:
            break

        last_cursor = last_response["data"]["fields"][-1]["cursor"]

        if last_cursor is None:
            break

        query["variables"]["cursor"] = last_cursor
