#!/bin/python3

import os
import urllib.parse
from datetime import date

import requests
import pandas

from plotting import plot_timeseries, box_plot_multiple_timeseries_by_freq, plot_multiple_timeseries_by_year, plot_stacked_bar_chart, plot_pie_chart

API_KEY = os.environ.get("API_KEY") or exit('API_KEY environment variable required')

BASE_URL = 'https://api.agrimetrics.co.uk/field-search?'

SEARCH_SHAPE_POLYGON = """geo.intersects(Location, geography'SRID=0;MultiLineString((-0.165482 51.992382,-0.175095 51.981492,-0.192947 51.974936,-0.189171 51.963196,-0.195866 51.950078,-0.167198 51.959388,-0.133553 51.941824,-0.096645 51.954627,-0.086002 51.966793,-0.102654 51.981704,-0.126858 51.992276,-0.165482 51.992382))'"""
SEARCH_SHAPE_CIRCLE = """geo.distance(Field/centroid,geography'SRID=0;Point(-0.138702 51.963196)') lt 3500"""

SEARCH_FILTER_PROPERTIES = """(Field/hasSownCrop/any(c: c/harvestYear eq 2018 and c/label eq 'Wheat'))"""
SEARCH_SELECT_PROPERTIES = [
    "Field/hasSoilLayer/hasChemicalProperty",
    "Field/hasSoilLayer/hasBiologicalProperty",
    "Field/hasSoilLayer",
    "Field/hasLongTermAverageMonthlyTotalRainfall",
    "Field/hasMonthlyTotalRainfall"
]


def main():
    search_url = generate_search_query(shape=SEARCH_SHAPE_CIRCLE, filter=SEARCH_FILTER_PROPERTIES, select=SEARCH_SELECT_PROPERTIES)
    print(f'Field Search URL: {search_url}\n')
    
    search_results = get_data(search_url)
    print(f"Found {search_results['totalResults']} fields.")
    
    first_10 = search_results['results'][:10]
    
    process_rainfall_data(first_10)
    process_soil_data(first_10)


def process_rainfall_data(data):

    dataseries = []

    # take first 10 results
    for i, result in enumerate(data):
        field_data = json_to_dataframe(result['hasMonthlyTotalRainfall']['hasDatapoint'])
        field_data = convert_year_month_columns_to_date(field_data)
        field_data["resultIndex"] = i
        dataseries.append(field_data)

    all_fields_data = pandas.concat(dataseries)

    # plot series for all fields
    box_plot_multiple_timeseries_by_freq(all_fields_data, ['month', 'year'], labels=['Monthly', 'Yearly'], title='Rainfall')
    plot_multiple_timeseries_by_year(all_fields_data, title='Yearly rainfall per field')

    # plot series for first field
    monthly_rainfall_for_first_field = all_fields_data[all_fields_data.resultIndex == 0]
    plot_timeseries(monthly_rainfall_for_first_field, title='3 years of rainfall for first field')

    # pretty print first field
    monthly_rainfall_for_first_field = monthly_rainfall_for_first_field[['year', 'month', 'value']].copy()
    print('\nMonthly rainfall for first field')
    print(monthly_rainfall_for_first_field.to_string(index=False))


def process_soil_data(data):
    soil_data = []

    for i, result in enumerate(data):
        field_soil_layer_data = result['hasSoilLayer']
        field_soil_data = json_to_dataframe(field_soil_layer_data)
        field_soil_data["resultIndex"] = i
        soil_data.append(field_soil_data)

    flattened_data = pandas.concat(soil_data, ignore_index=True)

    top_soil_data = flattened_data[flattened_data.hasSoilLayerType == 'http://data.agrimetrics.co.uk/soil-layer-types/topsoil'].dropna(axis=1)

    plot_columns = ['hasSoilTexture.clayPercentage', 'hasSoilTexture.siltPercentage', 'hasSoilTexture.sandPercentage']

    plot_stacked_bar_chart(
        data=top_soil_data,
        x='resultIndex',
        y=plot_columns,
        labels=[column.split(".")[1] for column in plot_columns],
        title="Soil composition by field"
    )

    df = pandas.DataFrame(top_soil_data['hasSoilTexture.hasSoilTextureType'].value_counts())

    plot_pie_chart(
        data=df['hasSoilTexture.hasSoilTextureType'], 
        labels=[soil_url_to_name(url) for url in df.index], 
        title='Fields by top soil type'
    )

    # pretty print
    pretty_data = flattened_data.rename(
        columns={
            'hasSoilLayerType': 'Layer',
            'hasSoilTexture.sandPercentage':'Sand %',
            'hasSoilTexture.clayPercentage':'Clay %',
            'hasSoilTexture.siltPercentage':'Silt %',
        }
    )
    pretty_data = pretty_data[['resultIndex', 'Layer', 'Sand %', 'Clay %', 'Silt %']].copy()
    pretty_data['Layer'] = pretty_data['Layer'].apply(lambda x: x.replace('http://data.agrimetrics.co.uk/soil-layer-types/',''))

    print('\nSoil layers')
    print(pretty_data.to_string(index=False))


def soil_url_to_name(url):
    return url.split("/")[-1]


def get_data(url):
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()


def generate_search_query(shape, filter, select):
    filter_query = f"{filter} and {shape}"
    select_query = ",".join(select)

    encoded_filter = urllib.parse.quote(filter_query)
    encoded_select = urllib.parse.quote(select_query)

    params = f"$filter={encoded_filter}&$select={encoded_select}"
    
    return f"{BASE_URL}{params}&subscription-key={API_KEY}"


def json_to_dataframe(data):
    return pandas.io.json.json_normalize(data)


def convert_year_month_columns_to_date(dataframe):
    dataframe.index = pandas.to_datetime(dataframe.apply(lambda x: datapoint_date_to_date(x), axis=1))
    return dataframe


def datapoint_date_to_date(datapoint):
    try:
        return date(year=int(datapoint['year']), month=int(datapoint['month']), day=1)
    except KeyError:
        return datapoint['dateTime']


if __name__ == "__main__":
    main()

