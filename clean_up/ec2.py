from __future__ import print_function
import boto3
from constants import AWS_REGIONS

def list_ec2_ids():
    filters = []
    instances = ec2.instances.filter(Filters=filters)

    instance_ids = []
    for instance in instances:
        instance_ids.append(instance.id)
        print('{}'.format(instance.id))
    print('Total EC2 instance = {}'.format(len(instance_ids)))
    return instance_ids

def delete_ec2_and_associates(ids=None):
    instances = ec2.instances.filter(InstanceIds=ids)
    for instance in instances:
        # delete key pair
        try:
            key_name = instance.key_name
            ec2.delete_key_pair(KeyName=key_name)
        except:
            pass
        
        # terminate instance
        instance.terminate()

if __name__ == '__main__':
    # session = boto3.Session(
    #     aws_access_key_id=AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    # )
    # ec2 = session.resource('ec2', region_name='us-west-2')

    # Use credential in AWS Config
    for region in AWS_REGIONS:
        print("Region: {}".format(region['name']))
        ec2 = boto3.resource('ec2', region_name=region['name'])
        ids = list_ec2_ids()
        delete_ec2_and_associates(ids)

