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
cp config.yaml.example config.yaml
# edit config.yaml
lambda invoke
```

Setting the `SNS_TOPIC_ARN` env var is optional.  Leave it unset to just run in "local" mode.

coinmarketcap API example:

```sh
curl -s -k "https://api.coinmarketcap.com/v1/ticker/ethereum/?convert=USD" | jq .
```

## Run it on AWS Lambda

Make sure your SNS topic + IAM role policy is configured in your account first (See Terraform section for more):

```sh
lambda deploy
```

## Terraform

There is some basic terraform configuration included to create the SNS topic, IAM role for Lambda execution + SNS publish.

```sh
cd terraform
terraform init
terraform plan
terraform apply
```

Note: Email subscriptions on SNS Topics are not supported by Terraform - they have to be added and verified manually.
