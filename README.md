# coin_watcher
Monitor and alert on cryptocurrency exchange rates via Lambda

# Development

How to setup a dev environment for this:

```sh
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

coinmarketcap API example:

```sh
curl -s -k "https://api.coinmarketcap.com/v1/ticker/ethereum/?convert=USD" | jq .
```
