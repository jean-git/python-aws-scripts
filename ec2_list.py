__author__ = "Jean Carlos Bezerra"
__maintainer__ = "Jean Carlos Bezerra"
__email__ = "jean2104@gmail.com"
__status__ = "Production"
"""
    Script to find EC2 in AWS
    You can filter by Region 
    You can choice returned data in a table or csv format
    Example of usaeg:
        python.exe .\ec2_list.py 
        python.exe .\ec2_list.py -o csv
        python.exe .\ec2_list.py -r us-east-1
"""
import datetime
import boto3
import sys, argparse
import json
from tabulate import tabulate

session = boto3.Session() # pega dados das configurações do aws cli

def get_ec2_regions_list():
    ec2 = session.client('ec2')

    response = ec2.describe_regions()

    regions = []
    for region in response['Regions']:

        regions.append(region['RegionName'])

    return regions


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def main(argv):

    global session

    ec2_infos = [['Region', 'AvailabilityZone', 'ImageId', 'InstanceId', 'InstanceType', 'PrivateDnsName', 'PublicDnsName', 'Tags', 'State']]
    regions = [argv.region] if argv.region != "" and argv.region != "all" else get_ec2_regions_list()
    for region in regions:

        print('\n------------- searching ec2 in aregion: ', region, '---------------')
        ec2 = session.client('ec2', region_name=region)

        # Filter example
        filter = [
            {
                'Name': 'instance-state-name',
                'Values': [
                        'running'
                ]
            },
            {
                'Name': 'tag:Environment',
                'Values': ['PROD']
            }
        ]

        filter = []
        response = ec2.describe_instances(

            Filters=filter,

        )

        print(f"Total found: {len(response['Reservations'])}")

        for instance in response['Reservations']:

            current_instance_data = instance['Instances'][0]

            tags = []
            for tag in current_instance_data['Tags']:
                tags.append(f"{tag.get('Key')}: {tag.get('Value')}")

            ec2_infos.append([  region, 
                                current_instance_data['Placement'].get('AvailabilityZone'), 
                                current_instance_data['ImageId'], 
                                current_instance_data['InstanceId'],
                                current_instance_data['InstanceType'],
                                current_instance_data['PrivateDnsName'],
                                current_instance_data['PublicDnsName'] if current_instance_data['PublicDnsName'] != "" else current_instance_data['PublicIpAddress'],
                                ",".join(tags),
                                current_instance_data['State'].get('Name'),
                                ])

    if argv.output == 'csv':
        for ec2 in ec2_infos:
            print(','.join(ec2))
    else:
        print(tabulate(ec2_infos,
                headers="firstrow", tablefmt="pretty")
                )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='EC2 List options')
    parser.add_argument('-o', '--output', dest='output', metavar='csv', default='table', choices=['table', 'csv'], help='type of return, csv or table' )
    parser.add_argument('-r', '--region', dest='region', metavar='us-west-1', default='all', choices=get_ec2_regions_list(), help='AWS EC2 Region' )

    args = parser.parse_args()

    main(args)
