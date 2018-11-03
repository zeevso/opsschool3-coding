"""
Ze'ev 2/11/2018
Exercises for the OOPS School 3, Coding in Python, Session 1, Assignment 1
Unit test for the exercise1 in  weather.py
    1. Delete output file if exists
    2. Run weather.py, checking if
        2.1 Output file opens as expected
        2.2 JSON is processed as expected
"""

import json
import os
from json import JSONDecodeError
from weather import exercise1 as weather_main

OUTPUT_FILE = 'weather.txt'


def test_main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    weather_main()

    assert os.path.exists(OUTPUT_FILE), 'The output file {} missed after running weather script'.format(OUTPUT_FILE)
    with open(OUTPUT_FILE) as file:
        try:
            weather_info = json.load(file)
        except JSONDecodeError:
            assert False, 'Could not deserialize JSON from file {}'.format(OUTPUT_FILE)

    assert 'id' in weather_info, 'Parameter id was expected from JSON'


if __name__ == '__main__':
    test_main()
