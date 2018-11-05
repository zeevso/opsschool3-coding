"""
Ze'ev 2/11/2018
Exercises for the OOPS School 3, Coding in Python, Session 1, Assignment 2

1. Read json format file
2. Prepare data structure of list of classes according to requirements
3. Fill in data structure
4. Dump data to yaml file
    4.1 Library 'PyYAML 3.13' should be installed separately to the standard Python distribution
 """

import json
import yaml

INPUT_FILE = 'my_list.json'
OUTPUT_FILE = 'my_list.yml'


class PersonsRange(object):
    def __init__(self, min_age, max_age, names=None):
        if names is None:
            names = []

        self.names = names
        self.min_age = min_age
        self.max_age = max_age

    def is_age_in_range(self, age):
        return self.min_age <= age < self.max_age


def read_json():
    with open(INPUT_FILE) as file:
        return json.load(file)


def init_ranges(data):
    buckets = data['buckets']
    buckets.append(0)
    buckets.sort()
    return(buckets)


def manage_person_ranges(buckets, data):
    persons_ranges = []
    for min_age, max_age in zip(buckets[:-1], buckets[1:]):
        persons_ranges.append(PersonsRange(min_age, max_age))

    biggest_age = max([age for name, age in data['ppl_ages'].items()])

    for name, age in data['ppl_ages'].items():
        inserted_name = False
        for bucket, persons_range in zip(buckets, persons_ranges):
            if persons_range.min_age <= age < persons_range.max_age:
                persons_range.names.append(name)
                inserted_name = True
                break

        if not inserted_name:
            biggest_age_on_bucket = max([persons_range.max_age for persons_range in persons_ranges])
            persons_ranges.append(PersonsRange(biggest_age_on_bucket, biggest_age, names=[name]))
    return persons_ranges


def write_output_file (persons_ranges):
    with open(OUTPUT_FILE, "w") as file:
         for persons_range in persons_ranges:
             print_dict = {'{}-{}'.format(persons_range.min_age, persons_range.max_age): persons_range.names}
             yaml.dump(print_dict, file, default_flow_style=False)


def main():
    data = read_json()
    buckets = init_ranges(data)
    persons_ranges = manage_person_ranges(buckets, data)
    write_output_file(persons_ranges)


if __name__ == '__main__':
    main()
