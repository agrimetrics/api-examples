#!/bin/python3

import os

import requests
import urllib

import json


API_KEY = os.environ.get("API_KEY") or exit('API_KEY environment variable required')
BASE_URL = "https://api.agrimetrics.co.uk/field-boundaries"

# Please note, these examples require an Agrimetrics subscription with premium credits.
# Running these examples for the first time will consume 6 premium credits,
# subsequent runs will not consume any more credits.


def main():
    get_all_field_boundaries_for_shape()
    get_all_field_boundaries_within_radius_as_geojson_feature_collection()
    get_field_boundary_by_field_id_as_geojson_feature()


def get_all_field_boundaries_for_shape():
    shape = "POLYGON((-0.35791397094726557 51.80370566913594,-0.3737926483154297 51.81853742720025,-0.38396358489990234 51.8139477982038,-0.3879976272583008 51.802246108975304,-0.36383628845214844 51.79999033214456,-0.35791397094726557 51.80370566913594))"

    url = f"{BASE_URL}?geometry={urllib.parse.quote(shape)}&op=within"
    print(f"\nBoundaries by shape URL (first page): {url}")

    all_results = fetch_all_results(url)

    print(f"Total results retrieved: {len(all_results)}")
    print(f"The first field id: {all_results[0]['id']}")
    print(f"The last field id: {all_results[-1]['id']}")
    print("Last result as JSON:")
    print(json.dumps(all_results[-1], indent=2))


def get_all_field_boundaries_within_radius_as_geojson_feature_collection():
    point  = (-0.363389293, 51.801963734) # (lon, lat)
    radius = 200 # meters
    url = f"{BASE_URL}?lon={point[0]}&lat={point[1]}&distance={radius}"
    print(f"\nBoundaries within radius URL: {url}")

    feature_collection = fetch_all_results_as_geojson(url)

    print(f"Number of fields boundaries (GeoJSON Features) within the circle: {len(feature_collection['features'])}")
    print(f"The first field id: {feature_collection['features'][0]['properties']['id']}")
    print(f"The last Field id: {feature_collection['features'][-1]['properties']['id']}")
    print("The last field boundary (as GeoJSON Feature):")
    print(json.dumps(feature_collection['features'][-1], indent=2))


def get_field_boundary_by_field_id_as_geojson_feature():
    field_id = "C6BgTxUxhMG_OCGrLGW8qw"
    url = f"{BASE_URL}/{field_id}"
    print(f"\nBoundary by field id URL: {url}")

    response = get_data(url=url, geojson=True)
    print(f"The boundary of field {field_id} (as GeoJSON Feature):")
    print(json.dumps(response['features'][0], indent=2))


# get all pages of results.
# We know that we have got all results when receive a page
# which has fewer than pageSize results.
def fetch_all_results(url, pageSize=100):
    pageNum = 1
    all_results = []
    while True:
        pageUrl = f"{url}&pageSize={pageSize}&pageNum={pageNum}"
        print(f"\tPage {pageNum} URL: {pageUrl}")

        response = get_data(url=pageUrl)

        page_of_results = response['results']
        all_results = all_results + page_of_results

        if len(page_of_results) < pageSize:
            print("\tReached last page of of results")
            break

        pageNum = pageNum + 1

    return all_results

# get all pages of GeoJSON FeatureCollection results.
# We know that we have got all results when receive a page
# which has fewer than pageSize features.
def fetch_all_results_as_geojson(url, pageSize=100):
    pageNum = 1
    all_features = []
    while True:
        pageUrl = f"{url}&pageSize={pageSize}&pageNum={pageNum}"
        print(f"\tPage {pageNum} URL: {pageUrl}")

        response = get_data(url=pageUrl, geojson=True)

        page_of_features = response['features']
        all_features = all_features + page_of_features

        if len(page_of_features) < pageSize:
            print("\tReached last page of of features")
            break

        pageNum = pageNum + 1

    # return re-built GeoJSON FeatureCollection structure
    return {
        'type': 'FeatureCollection',
        'features': all_features
    }


def get_data(url, geojson=False):
    headers = {
      'Ocp-Apim-Subscription-Key': API_KEY
    }
    if geojson:
        headers["accept"] = "application/geo+json"

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    main()

