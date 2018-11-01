from __future__ import print_function
import boto3
from constants import AWS_REGIONS

def list_s3_buckets(client):
    response = client.list_buckets()
    bucket_names = []
    for bucket in response['Buckets']:
        bucket_names.append(bucket['Name'])
        location = client.get_bucket_location(Bucket=bucket['Name'])
        print('{} {}'.format(location['LocationConstraint'], bucket['Name']))
    
    return bucket_names


def delete_s3_buckets(client, names=[]):
    for name in names:
        try:
            client.delete_bucket(Bucket =name)
            print('Deleting bucket {}'.format(name))
        except:
            pass


if __name__ == '__main__':
    for region in AWS_REGIONS:
        print("Region: {}".format(region['name']))
        client = boto3.client('s3', region_name=region['name'])
        names = list_s3_buckets(client)
        delete_s3_buckets(client, names)

