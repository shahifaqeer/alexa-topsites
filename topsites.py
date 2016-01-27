#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import sys
from math import ceil
from collections import defaultdict
import csv

BASE_URL='http://www.alexa.com/topsites/countries;%d/%s'

def get_top_country(country_code, number):

    data = defaultdict(list)
    page_numbers = int(ceil(number/25.0))

    for page_num in range(0, page_numbers):
        response = requests.get(BASE_URL % (page_num, country_code))

        soup = BeautifulSoup(response.text)
        bullets = soup.find_all('li', {'class':'site-listing'})

        for bullet in bullets:
            data['rank'].append(bullet.div.contents[0])
            data['site'].append(bullet.p.a.contents[0])

    filename = country_code + "_" + number + ".csv"
    with open("output/" + filename, 'w') as f:
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)

    return

if __name__ == '__main__':

    if len(sys.argv) != 3:
        sys.stderr.write('Usage: python topsites.py {COUNTRY-CODE, ALL} TOP-N\n')
        sys.exit(1)

    country_code = sys.argv[1].upper()
    number = int(sys.argv[2])

    if country_code == 'ALL':
        pass
    else:
        get_top_country(country_code, number)



