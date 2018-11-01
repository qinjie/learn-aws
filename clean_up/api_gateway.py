from __future__ import print_function
import boto3
import json
from time import sleep
from constants import AWS_REGIONS

def list_api_ids(client):
    client = boto3.client('apigateway')
    apis = client.get_rest_apis()
    api_ids = []
    print("============== List of API =============")
    for api in apis['items']:
        print("{} {}".format(api['id'],api['name']))
        api_ids.append(api['id'])

    return api_ids

def delete_apis(client, api_ids=[]):
    for api_id in api_ids:
        print("Deleting API with ID {}".format(api_id))
        try:
            response = client.delete_rest_api(restApiId=api_id)
            print('{}'.format(response))
        except Exception as e:
            print(str(e))
        
        # pause for 60 second to avoid "Too Many Requests" error
        sleep(60)


if __name__ == '__main__':
    for region in AWS_REGIONS:
        print("Region: {}".format(region['name']))
        client = boto3.client('apigateway', region_name=region['name'])
        api_ids = list_api_ids(client)
        delete_apis(client, api_ids)
