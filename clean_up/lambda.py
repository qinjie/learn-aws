from __future__ import print_function
import boto3
from constants import AWS_REGIONS

def list_lambda_names(client):
    response = client.list_functions()
    function_names = []
    for function in response['Functions']:
        function_names.append(function['FunctionName'])
        print(function['FunctionName'])
    
    return function_names


def delete_lambda_functions(client, names=None):
    for name in names:
        try:
            client.delete_function(FunctionName=name)
            print('Deleting function {}'.format(name))
        except:
            pass


if __name__ == '__main__':
    for region in AWS_REGIONS:
        print("Region: {}".format(region['name']))
        client = boto3.client('lambda', region_name=region['name'])
        names = list_lambda_names(client)
        delete_lambda_functions(client, names)

