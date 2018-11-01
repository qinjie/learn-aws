from __future__ import print_function
import boto3
import json
from constants import AWS_REGIONS

def delete_sns_topics(client):
    response = client.list_topics()
    arns = []
    for topic in response['Topics']:
        arns.append(topic['TopicArn'])
        topic_attrs = client.get_topic_attributes(TopicArn=topic['TopicArn'])
        print('{} {}'.format(topic_attrs['DisplayName'], topic_attrs['TopicArn']))
        
        try:
            client.delete_topic(TopicArn=topic['TopicArn'])
        except Except as e:
            print(str(e))
    return arns


def delete_sns_subscriptions(client):
    response = client.list_subscriptions(NextToken='')
    print('{}'.format(json.dumps(response)))
    for subscription in response['Subscriptions']:
        print('{}'.format(json.dumps(subscription)))
        try:
            client.unsubscribe(SubscriptionArn = subscription['SubscriptionArn'])
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    for region in AWS_REGIONS:
        print("Region: {}".format(region['name']))
        client = boto3.client('sns', region_name=region['name'])
        arns = delete_sns_topics(client)
        delete_sns_subscriptions(client)

