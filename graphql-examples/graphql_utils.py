import os
import requests


API_KEY = os.environ.get("API_KEY") or exit('API_KEY environment variable required')
BASE_URL = "https://api.agrimetrics.co.uk/graphql"


def get_data(query):
    response = requests.post(
        url=BASE_URL,
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "ocp-apim-subscription-key": API_KEY,
        },
        json=query,
    )

    response.raise_for_status()
    return response.json()


def get_paged_data(query, data_extractor, cursor_extractor):
    while True:
        last_response = get_data(query)

        data = data_extractor(last_response)
        yield data

        if not data:
            break

        last_cursor = cursor_extractor(last_response)

        if last_cursor is None:
            break

        query["variables"]["cursor"] = last_cursor
