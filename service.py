#!/usr/bin/env python

import requests
from IPython import embed

BASE_API_URI = 'https://api.coinmarketcap.com/v1/'
HEADERS = { 'Accept': 'application/json',
            'Content-Type': 'application/json' }

def get_data():
    r = requests.get(BASE_API_URI + "ticker", headers=HEADERS)
    return r.json()

# main
def handler(event, context):
    checks = event.get('checks')
    alert_email = event.get('alert_email')

    if checks:
        print("Querying...")
        data = get_data()

        alerts = []
        for c in checks:
            cur = next(item for item in data if item['symbol'] == c['coin'])
            print( c['coin'], "\n", {k: cur.get(k, None) for k in (
                'id', 'symbol', 'price_usd', 'price_usd', 'percent_change_1h'
                'percent_change_24h', 'percent_change_7d', 'last_updated')} )
    else:
        print("No checks defined.  Quit.")

    print("Done")
