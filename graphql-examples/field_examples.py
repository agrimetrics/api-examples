#!/bin/python3

from datetime import datetime
import json

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
    for result in get_paged_data(query):
        fields.extend(result["data"]["fields"])

    return {"data": {"fields": fields}}


def main():
    pretty_print(get_field_by_id())
    pretty_print(query_soil_by_polygon())
    pretty_print(query_soil_by_point())
    pretty_print(query_daily_rainfall_for_field_for_current_month())
    pretty_print(query_ids_for_large_area())


if __name__ == "__main__":
    main()
