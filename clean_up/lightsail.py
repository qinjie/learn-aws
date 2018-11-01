from __future__ import print_function
import boto3

def list_lightsail_names(client):
    response = client.get_instances()
    instances = response['instances']
    instance_names = []
    for instance in instances:
        instance_names.append(instance['instanceName'])
        print('{}'.format(instance['instanceName']))
    return instance_names

def delete_lightsail_instance(client):
    names = list_lightsail_names(client)
    for name in names:
        # delete key pair
        try:
            response = client.delete_instance(instanceName=name)
        except Exception as e:
            print(str(e))

def delete_lightsail_snapshots(client):
    response = client.get_instance_snapshots()
    snapshots = response['instanceSnapshots']
    for snapshot in snapshots:
        client.delete_instance_snapshot(instanceSnapshotName = snapshot['name'])
    

if __name__ == '__main__':
    # session = boto3.Session(
    #     aws_access_key_id=AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    # )
    # ec2 = session.resource('lightsail', region_name='us-west-2')

    # Use credential in AWS Config
    client = boto3.client('lightsail')
    delete_lightsail_instance(client)
    delete_lightsail_snapshots(client)

