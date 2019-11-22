#!/bin/python3

import os
from datetime import date

import requests
import pandas

from plotting import plot_timeseries

API_KEY = os.environ.get("API_KEY") or exit('API_KEY environment variable required')


def main():
    coordinates = {
        "lat": 51.801963734,
        "lon": -0.363389293,
    }

    field_response = find_field(coordinates)

    print(f"Field ID: {field_response['@id']}")

    process_field_trends_rainfall(field_response)
    process_field_forecasts_temperature(field_response)
    process_field_facts_soil(field_response)


def process_field_trends_rainfall(field_finder_response):
    # Monthly Rainfall
    field_trends_url = get_api_url(field_finder_response, 'field-trends')
    print(f"\nField Trends URL: {field_trends_url}")

    trends_result = get_data(field_trends_url)
    monthly_rainfall = json_to_dataframe(trends_result['hasMonthlyTotalRainfall']['hasDatapoint'])
    monthly_rainfall = monthly_rainfall[['year', 'month', 'value']].copy()
    monthly_rainfall = convert_year_month_columns_to_date(monthly_rainfall)

    plot_timeseries(monthly_rainfall, title='Monthly rainfall for last 3 years')


    # the data can be output as csv by using to_csv function instead
    print('\nMonthly rainfall for last 3 years')
    print(monthly_rainfall.to_string(index=False))


def process_field_forecasts_temperature(field_finder_response):

    # Get daily maximum temperatures
    field_forecasts_url = get_api_url(field_finder_response, 'field-forecasts')
    print(f"\nField Forecasts URL: {field_forecasts_url}")

    forecast_result = get_data(field_forecasts_url)
    daily_forecast_maximum_temperature = json_to_dataframe(forecast_result['hasForecastDailyMaximumTemperature']['hasDatapoint'])
    daily_forecast_maximum_temperature = daily_forecast_maximum_temperature[['dateTime', 'value']].copy()
    daily_forecast_maximum_temperature = convert_dateTime_columns_to_datetime(daily_forecast_maximum_temperature)

    plot_timeseries(daily_forecast_maximum_temperature, title='Daily Maximum Temperature')

    print('\nDaily Maximum Temperature')
    print(daily_forecast_maximum_temperature.to_string(index=False))


def process_field_facts_soil(field_finder_response):
    # Soil layers
    field_facts_url = get_api_url(field_finder_response, 'field-facts')
    print(f"\nField Facts URL: {field_facts_url}")

    facts_result = get_data(field_facts_url)

    soil_layers = json_to_dataframe(facts_result['hasSoilLayer'])

    # Select and reformat for nicer display...
    soil_layers.rename(
        columns={
            'hasSoilLayerType': 'Layer',
            'hasSoilTexture.sandPercentage':'Sand %',
            'hasSoilTexture.clayPercentage':'Clay %',
            'hasSoilTexture.siltPercentage':'Silt %',
        },
        inplace=True
    )
    soil_layers = soil_layers[['Layer', 'Sand %', 'Clay %', 'Silt %']].copy()
    soil_layers['Layer'] = soil_layers['Layer'].apply(lambda x: x.replace('http://data.agrimetrics.co.uk/soil-layer-types/',''))

    print('\nSoil Layers')
    print(soil_layers.to_string(index=False))


def get_data(url):
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()


def find_field(coordinates):
    url = f"https://api.agrimetrics.co.uk/field-finder?lat={coordinates['lat']}&lon={coordinates['lon']}&subscription-key={API_KEY}"
    return get_data(url)


def get_api_url(field_response, field_api):
    return f"{field_response['_links'][f'ag:api:{field_api}']['href']}?subscription-key={API_KEY}"


def json_to_dataframe(data):
    return pandas.io.json.json_normalize(data)


def convert_year_month_columns_to_date(dataframe):
    dataframe.index = pandas.to_datetime(dataframe.apply(lambda x: datapoint_date_to_date(x), axis=1))
    return dataframe


def convert_dateTime_columns_to_datetime(dataframe):
    dataframe.index = pandas.to_datetime(dataframe['dateTime'])
    return dataframe


def datapoint_date_to_date(datapoint):
    try:
        return date(year=int(datapoint['year']), month=int(datapoint['month']), day=1)
    except KeyError:
        return datapoint['dateTime']


if __name__ == "__main__":
    main()
