#!/bin/python3

from datetime import datetime
import json

import pandas

from graphql_utils import get_paged_data, get_data

POINT_LOCATION = {"type": "Point", "coordinates": [-0.138702, 51.963196]}

POLYGON_LOCATION = {
    "type": "Polygon",
    "coordinates": [
        [
            [-0.165482, 51.992382],
            [-0.175095, 51.981492],
            [-0.192947, 51.974936],
            [-0.189171, 51.963196],
            [-0.195866, 51.950078],
            [-0.167198, 51.959388],
            [-0.133553, 51.941824],
            [-0.096645, 51.954627],
            [-0.086002, 51.966793],
            [-0.102654, 51.981704],
            [-0.126858, 51.992276],
            [-0.165482, 51.992382],
        ]
    ],
}


def pretty_print(data, indent=2):
    if data:
        print(json.dumps(data, indent=indent))
        try:
            print(f"Number of results: {len(data['data']['fields'])}")
        except TypeError:
            print(f"No results or invalid request")
    else:
        print("No results")


def query_soil_by_polygon():
    """
    Get the soil information for the area specified by a custom polygon.
    """
    query = {
        "query": """query SoilPolygonQuery($location: LocationFilter!) {
            fields(filter: {location: $location}
            ) {
                id
                area
                altitude
                soil {
                    topSoil {
                        texture {
                            type
                        }
                    }
                }
            }
        }""",
        "variables": {"location": POLYGON_LOCATION},
        "operationName": "SoilPolygonQuery",
    }

    return get_data(query)


def query_soil_by_point():
    """
    Get the soil information for the area within 3500m of the default point location.
    """
    query = {
        "query": """query SoilPointQuery($location: LocationFilter!) {
            fields(filter: {location: $location distance: 3500}) {
                id
                soil {
                    topSoil {
                        texture {
                            type
                        }
                    }
                }

            }
        }""",
        "variables": {"location": POINT_LOCATION},
        "operationName": "SoilPointQuery",
    }

    return get_data(query)


def get_field_by_id():
    """
    Get the area, altitude and soil information for a specific field
    """
    query = {
        "query": """query MyQuery1($fieldId: ID!) {
            fields(filter: {id: $fieldId}) {
                id
                area
                altitude
                soil {
                    topSoil {
                        texture {
                            type
                        }
                    }
                }
            }
        }""",
        "variables": {"fieldId": "agfd:zlrdrtL7m0-1RsAf7TvSww"},
    }

    return get_data(query)


def query_daily_rainfall_for_field_for_current_month():
    """
    For a given field id, get all the total daily rainfall since the start of the month.
    """
    query = {
        "query": """query RainfallQuery($fieldId: ID!, $startDate: Date!) {
            fields(filter: {id: $fieldId}) {
                id
                weatherObservations(dateRange: {startDate: $startDate}) {
                    rainfallTotalDaily {
                        value
                    }
                }
            }
        }""",
        "variables": {
            "fieldId": "agfd:zlrdrtL7m0-1RsAf7TvSww",
            "startDate": datetime.now().replace(day=1).strftime("%Y-%m-%d"),
        },
        "OperationName": "RainfallQuery",
    }

    return get_data(query)


def extract_fields(response):
    return response["data"]["fields"]


def extract_fields_cursor(response):
    return response["data"]["fields"][-1]["cursor"]


def get_paged_field_data(query):
    return get_paged_data(query, data_extractor=extract_fields, cursor_extractor=extract_fields_cursor)


def query_ids_for_large_area():
    """
    Get the ids of all fields that lie within a 10000m radius of the default point location.

    Note that this example uses a cursor to page through all the results.
    """
    query = {
        "query": """query LargeSearchArea($location: LocationFilter!, $cursor: String) {
            fields(filter: {location: $location distance: 10000}, after: $cursor) {
                id
                cursor
            }
        }""",
        "variables": {"location": POINT_LOCATION, "cursor": None},
        "OperationName": "LargeSearchArea",
    }

    fields = []
    for result in get_paged_field_data(query):
        fields.extend(result)

    return {"data": {"fields": fields}}


def query_historic_rainfall_for_fields():
    """
    Get the historic rainfall for all fields that lie within a 1000m radius of the default point location.

    Note that this example uses a cursor to page through all the rainfall data results.
    """
    query = {
        "query": """query SampleFields($location: LocationFilter!) {
            fields(filter: {location: $location distance: 1000}) {
                id
            }
        }""",
        "variables": {"location": POINT_LOCATION},
        "OperationName": "SampleFields",
    }

    fields = get_data(query)

    for field in fields["data"]["fields"]:
        field["weatherObservations"] = {
            "rainfallTotalDaily": get_rainfall_for_field(field["id"], start_date="2019-05-01")
        }

    return fields


def extract_rainfall_total_daily(response):
    return response["data"]["node"]["weatherObservations"]["rainfallTotalDaily"]


def extract_weather_observations_cursor(response):
    return response["data"]["node"]["weatherObservations"]["cursor"]


def get_paged_rainfall_data(query):
    return get_paged_data(
        query, data_extractor=extract_rainfall_total_daily, cursor_extractor=extract_weather_observations_cursor
    )


def get_rainfall_for_field(id, start_date):
    query = {
        "query": """query FieldRainfall($id: ID!, $startDate: Date!, $cursor: String) {
            node(id: $id) {
                ... on Field {
                    weatherObservations(dateRange: {startDate: $startDate}, after: $cursor) {
                        cursor
                        rainfallTotalDaily {
                            value
                            dateTime
                        }
                    }
                }
            }
        }""",
        "OperationName": "FieldRainfall",
        "variables": {"id": id, "startDate": start_date},
    }

    rainfall_data = []
    for result in get_paged_rainfall_data(query):
        rainfall_data.extend(result)

    return rainfall_data


def main():
    pretty_print(get_field_by_id())
    pretty_print(query_soil_by_polygon())
    pretty_print(query_soil_by_point())
    pretty_print(query_daily_rainfall_for_field_for_current_month())
    pretty_print(query_ids_for_large_area())
    pretty_print(query_historic_rainfall_for_fields())


if __name__ == "__main__":
    main()
