#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import sys, os
from math import ceil
from collections import defaultdict
import csv

BASE_URL='http://www.alexa.com/topsites/countries;%d/%s'
COUNTRY_URL='http://www.alexa.com/topsites/countries'

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

    filename = country_code + "_" + str(number) + ".csv"
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

    if not os.path.exists('output'):
        os.makedirs('output')

    if country_code == 'ALL':
        response = requests.get(COUNTRY_URL)
        soup = BeautifulSoup(response.text)
        uls = soup.find_all('ul', {'class': 'countries span3'})
        for ul in uls:
            #print ul
            bullets = ul.find_all('li')
            for bullet in bullets:
                country_code = bullet.a['href'].split('/')[-1]
                print country_code, bullet.a.contents[0]
                get_top_country(country_code, number)
    else:
        get_top_country(country_code, number)



