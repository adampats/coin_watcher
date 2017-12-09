# coin_watcher
Monitor and alert on cryptocurrency exchange rates via Lambda

# dev

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

coinmarketcap example:
```sh
curl -s -k "https://api.coinmarketcap.com/v1/ticker/ethereum/?convert=USD" | jq .
```
