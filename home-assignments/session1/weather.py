"""
Ze'ev 2/11/2018
Exercises for the OOPS School 3, Coding in Python, Session 1, Assignment 1

1. Check location by IP and get the weather data using REST APIs. Write weather data to the text file.
    1.1 Library 'requests' should be installed separately to the standard Python distribution
    1.2 Use an unit test.py to check assignment 1
2. Create a list with at least 10 cities and print their current weather in predefined format
    2.1 File countryinfo contains a small GIS DB found on Internet. Should be added to the project

Ze'ev 5/11/2018
try - except added
"""

import json
import requests
import countryinfo

OUTPUT_FILE = 'weather.txt'

def get_public_ip():
    try:
        r = requests.get("http://jsonip.com/").json()
    except requests.exceptions.RequestException as e:
        print(e)
        print(str(e))
        exit(1)

    return r["ip"]


def get_current_location(ip):
    try:
        r = requests.get('http://api.ipstack.com/{ip}'.format(ip=ip),
                      params={'access_key': 'ccc24d2f35243ddc0417ba4acab09a52'}).json()
    except requests.exceptions.RequestException as e:
        print(e)
        print(str(e))
        exit(1)

    return r['city'] + ',' + r['country_code']


def get_local_weather(location):
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather',
                      params={'q': location, 'units': 'metric', 'APPID': 'a08359a0cfaf6172ada114041887b2f0'}).json()
    except requests.exceptions.RequestException as e:
        print(e)
        print(str(e))
        exit(1)

    return r


def get_country_by_code(country_code, countries):
    for country in countries:
        if country['code'] == country_code:
            country_name = country['name']
            return (country_name)


def weather_conditions_at_cities():
    cities = ['Vienna', 'Paris', 'Berlin', 'Brussels', 'Madrid', 'Barcelona', 'Riga', 'Prague', 'Dublin', 'Warsaw']
    countries = countryinfo.countries

    for city in cities:
        weather_data = get_local_weather(city)
        country_code = weather_data['sys']['country']
        try:
            country_name = get_country_by_code(country_code.upper(), countries)
        except TypeError:
            print ('{} not found'.format(city))
        print('The weather in {city}, {country} is {t:2.0f} degree °C'.format
              (city=city, country=country_name,t=weather_data['main']['temp']))


def exercise1():
    ip = get_public_ip()
    location = get_current_location(ip)
    weather_data = get_local_weather(location)
    try:
        with open(OUTPUT_FILE, "w") as file:
            json.dump(weather_data, file, indent=2)
    except IOError:
        print('Error writing to file {}'.format(OUTPUT_FILE))


def exercise2():
    weather_conditions_at_cities()


if __name__ == '__main__':
    exercise1()
    exercise2()

