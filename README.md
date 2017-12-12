# coin_watcher
Monitor and alert on cryptocurrency exchange rates via Lambda

Built using [python-lambda](https://github.com/nficano/python-lambda).

## Run it local

How to setup a dev environment + run this:

```sh
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
export SNS_TOPIC_ARN='arn:aws:sns:us-west-2:111111111111:example'
lambda invoke
```

Setting the `SNS_TOPIC_ARN` env var is optional.  Leave it unset to just run in "local" mode.

coinmarketcap API example:

```sh
curl -s -k "https://api.coinmarketcap.com/v1/ticker/ethereum/?convert=USD" | jq .
```

## Run it on AWS Lambda

```sh
lambda deploy
```
