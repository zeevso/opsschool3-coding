""""
Ze'ev 10/11/2018
Exercises for the OOPS School 3, Coding in Python, Session 2, Assignment 1

Command line arguments follow the following format -
    `python cli.py [] CITY`
CITY is a mandatory argument
Options:
    [--period <num-of-days> -f]
num-of-days may be in format TODAY+n
num-of-days default value is TODAY == 1
Use -f to override default to Fahrenheit measurements
"""

import click
import requests
from weather import Weather, Unit

unit_dict = {
    False: (Unit.CELSIUS, 'Celsius'),
    True:  (Unit.FAHRENHEIT, 'Fahrenheit')
}


def parse_unit(unit_flag):
    unit, unit_full_name = unit_dict.get(unit_flag)

    return unit, unit_full_name


def parse_period(period):
    days = 0

    if period == 'TODAY':
        days = 1
    elif '+' in period:
        split_str = period.split('+')
        days_digit = split_str[-1]
        if days_digit.isdigit():
            days = int(days_digit) + 1

    if days == 0:
        print('Invalid value in period: expected TODAY+n. Defaulted to TODAY')
        days = 1

    return days


@click.command()
@click.argument('city', nargs=-1)
@click.option('--period', default='TODAY', help='period in format TODAY+n')
@click.option('-f', is_flag=True, help='-f for Fahrenheit')
def parse_command(city, period, f):
    city = ' '.join(city)
    return city, period, f


def main():
    city, period, unparsed_unit = parse_command(standalone_mode=False)
    unit, unit_full_name = parse_unit(unparsed_unit)
    days_in_forecast = parse_period(period)

    try:
        weather = Weather(unit)
    except AttributeError:
        print('Could not load weather')
        return

    try:
        forecasts = weather.lookup_by_location(city)
    except requests.exceptions.HTTPError:
        print('Error getting weather forecast')
        return

    day_today = True
    days_counter = 0
    try:
        for day in forecasts.forecast[:days_in_forecast]:
            if day_today:
                date_to_print = 'Today'
            else:
                date_to_print = 'On ' + day.date

            print(
            '{date} the weather in {city} is {condition} with temperature trailing from {low_temp} to {high_temp} in {unit}'.
                format(date=date_to_print,
                       city=city,
                       condition=day.text.lower(),
                       low_temp=day.low,
                       high_temp=day.high,
                       unit=unit_full_name))
            days_counter += 1

            if day_today and (days_in_forecast-1) != 0:
                print()
                print('Forecast for the next {} days)'.format(days_in_forecast-1))
                print()
                day_today = False
    except KeyError:
        print('Could not print forecasts. Invalid argument')
        return

    if days_counter < (days_in_forecast - 1):
        print('Sorry! The maximum days of forecast is {} :('.format(days_counter))


if __name__ == '__main__':
    main()
