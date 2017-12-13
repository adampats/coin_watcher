#!/usr/bin/env python

import requests
import time
import os
import json
import boto3
from botocore.exceptions import ClientError

BASE_API_URI = 'https://api.coinmarketcap.com/v1/'
HEADERS = { 'Accept': 'application/json',
            'Content-Type': 'application/json' }
VERBOSE = True
MSG_SUBJECT = 'coin_watcher alert'

def get_data():
    r = requests.get(BASE_API_URI + "ticker", headers=HEADERS)
    return r.json()

def send_sns(topic_arn, msg, subject):
    try:
        client = boto3.client('sns')
        arn = client.get_topic_attributes(TopicArn = topic_arn)
        resp = client.publish(
            TopicArn = topic_arn,
            Subject = subject,
            Message = msg)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NotFound':
            print("SNS Topic,", topic_arn, "not found.  Message not sent.")
            raise Exception(e)
        if e.response['Error']['Code'] == 'AuthorizationError':
            print("Not authorized to publish to SNS, check IAM policies.")
            raise Exception(e)
        else:
            print("Unexpected error:", e)

# main
def handler(event, context):
    verbose = VERBOSE
    checks = event.get('checks')
    alert_email = event.get('alert_email')
    if 'SNS_TOPIC_ARN' in os.environ:
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    else:
        sns_topic_arn = 'local'

    if checks:
        print("Querying...")
        data = get_data()

        alerts = []
        alert_subject = ""
        for c in checks:
            cur = next(item for item in data if item['symbol'] == c['coin'])

            cur = {k: cur.get(k, None) for k in (
                'id', 'symbol', 'price_usd', 'price_usd', 'percent_change_1h',
                'percent_change_24h', 'percent_change_7d', 'last_updated')}
            cur['last_updated'] = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(int(cur['last_updated'])) )

            if verbose: print("=", cur['symbol'], "=\n", cur)

            if abs(float(cur['percent_change_1h'])) >= float(c['pct_threshold_1h']):
                cur['coin_watcher_trigger'] = '1h'
                alerts.append(cur)
                if verbose: print(cur['symbol'], "1h threshold triggered!")

            if abs(float(cur['percent_change_24h'])) >= float(c['pct_threshold_24h']):
                cur['coin_watcher_trigger'] = '24h'
                alerts.append(cur)
                if verbose: print(cur['symbol'], "24h threshold triggered!")

        if alerts != []:
            alert_subject = " - " + alerts[0]['symbol'] + " - " + \
                alerts[0]['coin_watcher_trigger']
        sns_msg = json.dumps(alerts, indent=4, sort_keys=True)
        if verbose:
            print("Alerts", alert_subject, "\n", sns_msg)
        if sns_topic_arn == 'local':
            print("Skipping SNS publish since SNS_TOPIC_ARN environment " + \
                  "variable is not specified.")
        else:
            send_sns(sns_topic_arn, sns_msg, MSG_SUBJECT + alert_subject)

    else:
        print("No checks defined.  Quit.")
