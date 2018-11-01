from __future__ import print_function
import boto3
import json

def list_role_names(client):
    roles = client.list_roles()
    role_names = []
    for role in roles['Roles']:
        print('{} {}'.format(role['RoleId'], role['RoleName']))
        role_names.append(role['RoleName'])
    return role_names
 

def delete_roles(client, role_names):
    for name in role_names:
        role = client.get_role(RoleName = name)
        print(json.dumps(role, default=str))
        print('Detach policies for role {}'.format(name))

        profiles = client.list_instance_profiles_for_role(RoleName=name)
        print(json.dumps(profiles, default=str))
        for profile in profiles['InstanceProfiles']:
            client.remove_role_from_instance_profile(InstanceProfileName=profile['InstanceProfileName'], RoleName=name)
            client.delete_instance_profile(InstanceProfileName=profile['InstanceProfileName'])
        
        policies = client.list_role_policies(RoleName=name)
        print(json.dumps(policies, default=str))
        for policy_name in policies['PolicyNames']:
            try:
                response = client.delete_role_policy(RoleName=name, PolicyName=policy_name)
                print(response)
            except Exception as e:
                print("Exception: {}".format(str(e)))

        try:
            print('Delete role {}'.format(name))
            client.delete_role(RoleName = name)
        except Exception as e:
            print("Exception: {}".format(str(e)))


if __name__ == '__main__':
    client = boto3.client('iam')
    role_names = list_role_names(client)
    delete_roles(client, role_names)
