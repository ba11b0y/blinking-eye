import grequests
import argparse
import os
from platform import system as os_name
import pandas as pd
import requests
import sqlite3

lookup_data = []

def gen_list_urls(relay_data, points):
    urls = ['http://ip-api.com/json/'+row[1] for row in relay_data[:points]]
    return urls


def lookup(urls):
    """
    :param: ipaddress to look up
    :returns: A dict containing all information post lookup
    """
    res = (grequests.get(u) for u in urls)
    consol_res = grequests.map(res)
    return consol_res

def index_data_from_cache_file(path):
    """
    For reading from cache.sqlite file
    :param: path to the cache file
    :returns: A list containing tuples where each tuple represents a row [(), (), ()]

    """

    conn = sqlite3.connect(path)
    c = conn.cursor()
    relay_data = c.execute('SELECT * FROM relays')
    relay_data = relay_data.fetchall()
    return relay_data

def gen_data_frame(path, points):
    raw_data = index_data_from_cache_file(path)
    urls = gen_list_urls(raw_data, points)
    all_responses = lookup(urls)
    cities = []
    countries = []
    lats = []
    longs = []
    for res in all_responses:
        res_data = res.json()
        cities.append(res_data["city"])
        lats.append(res_data["lat"])
        longs.append(res_data["lon"])
        countries.append(res_data["country"])
    
    df = pd.DataFrame({'City': cities,
    'Country': countries,
    'Latitude': lats,
    'Longitude': longs}
    )
    return df




