import boto3

ec2_client_singapore = boto3.client('ec2', region_name="ap-southeast-1")
ec2_resource_singapore = boto3.resource('ec2', region_name="ap-southeast-1")

ec2_client_sydney = boto3.client('ec2', region_name="ap-southeast-2")
ec2_resource_sydney = boto3.resource('ec2', region_name="ap-southeast-2")

instances_ids_singapore = []
instances_ids_sydney = []

reservations_paris = ec2_client_singapore.describe_instances()['Reservations']
for res in reservations_paris:
    instances = res['Instances']
    for ins in instances:
        instances_ids_singapore.append(ins['InstanceId'])


response = ec2_resource_singapore.create_tags(
    Resources=instances_ids_singapore,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)


reservations_frankfurt = ec2_client_sydney.describe_instances()['Reservations']
for res in reservations_frankfurt:
    instances = res['Instances']
    for ins in instances:
        instances_ids_sydney.append(ins['InstanceId'])


response = ec2_resource_sydney.create_tags(
    Resources=instances_ids_sydney,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)



