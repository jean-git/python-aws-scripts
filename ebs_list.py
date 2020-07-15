__author__ = "Jean Carlos Bezerra"
__maintainer__ = "Jean Carlos Bezerra"
__email__ = "jean2104@gmail.com"
__status__ = "Production"
"""
    Script to list EBS in AWS
    You can filter by Region 
    You can choice returned data in a table or csv format
    Example of usage:
        python ebs_list.py 
        python ebs_list.py -o csv
        python ebs_list.py -r us-east-1
"""
import datetime
import boto3
import sys, argparse
import json
from tabulate import tabulate

session = boto3.Session() # get default configurations of aws cli

def get_ec2_regions_list():
    ec2 = session.client('ec2')

    response = ec2.describe_regions()

    regions = []
    for region in response['Regions']:

        regions.append(region['RegionName'])

    return regions


def main(argv):

    global session

    ec2_infos = [['Region', 'AvailabilityZone', 'VolumeId', 'InstanceId', 'Size(GB)', 'Iops', 'VolumeType', 'State', 'Tags']]
    regions = [argv.region] if argv.region != "" and argv.region != "all" else get_ec2_regions_list()
    for region in regions:

        print('\n------------- searching ebs in a region: ', region, '---------------')
        ec2 = session.client('ec2', region_name=region)

        filter = []
        response = ec2.describe_volumes(

            #Filters=filter,

        )

        print(f"Total found: {len(response['Volumes'])}")

        for volume in response['Volumes']:

            current_ebs_data = volume['Attachments'][0]

            tags = []
            for tag in volume.get('Tags', []):
                tags.append(f"{tag.get('Key')}: {tag.get('Value')}")

            ec2_infos.append([  region, 
                                volume.get('AvailabilityZone'), 
                                current_ebs_data.get('VolumeId'), 
                                current_ebs_data.get('InstanceId'), 
                                volume['Size'], 
                                volume['Iops'], 
                                volume['VolumeType'], 
                                volume['State'], 
                                ','.join(tags), 
                                ])

    if argv.output == 'csv':
        for ec2 in ec2_infos:
            print(','.join(ec2))
    else:
        print(tabulate(ec2_infos,
                headers="firstrow", tablefmt="grid")
                )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='EC2 List options')
    parser.add_argument('-o', '--output', dest='output', metavar='csv', default='table', choices=['table', 'csv'], help='type of return, csv or table' )
    parser.add_argument('-r', '--region', dest='region', metavar='us-west-1', default='all', choices=get_ec2_regions_list(), help='AWS EC2 Region' )

    args = parser.parse_args()

    main(args)
