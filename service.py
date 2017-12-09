#!/usr/bin/env python

import requests

BASE_API_URI = 'https://api.coinmarketcap.com/v1/'
HEADERS = { 'Accept': 'application/json', 'Content-Type': 'application/json' }

# Get price stats for individual coin:currency
# pass arg as string, e.g. "BTC:USD"
def get_spot_price(currency_pair):
    coin, fiat = currency_pair.split(':')
    path = "ticker/" + CURRENCY_MAP[coin] + "/?convert=" + fiat
    print(BASE_API_URI + path)
    r = requests.get(BASE_API_URI + path, headers=headers)
    return r.text

# main
def handler(event, context):
    print("Querying...")
    currency_pairs = event.get('currency_pairs')

    if type(currency_pairs):
        for pair in currency_pairs:
            print("Checking", pair, "...")
            current = get_spot_price(pair)
            print(current)

    print "Done."
