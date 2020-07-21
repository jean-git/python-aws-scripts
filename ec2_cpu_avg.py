__author__ = "Jean Carlos Bezerra"
__maintainer__ = "Jean Carlos Bezerra"
__email__ = "jean2104@gmail.com"
__status__ = "Production"
"""
    Script to list EC2 instances and get CPU AVG in AWS
    You can filter by Region 
    You can filter by number of last days - defaul value is last 7 days
    You can choice returned data in a table or csv format
    Example of usage:
        python ec2_list.py 
        python ec2_list.py -o csv
        python ec2_list.py -r us-east-1
        python ec2_list.py -r us-east-1 -d 3
"""
import datetime
import boto3
import sys, argparse
import json
from tabulate import tabulate
from datetime import datetime, timedelta

session = boto3.Session() # get default configurations of aws cli

def get_cpu_util( instanceID, last_days = 7):

    cloudwatch = session.client('cloudwatch')

    start_time = datetime.utcnow() - timedelta(days=last_days)
    end_time = datetime.utcnow()

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceID
            },
        ],
        MetricName="CPUUtilization",
        StartTime = start_time,
        EndTime = end_time,
        Period=(86400),
        Statistics=[
            'Average'
        ],
    )

    avg = 0.0
    tot_metrics = float(len(response.get('Datapoints', [])))
    for item in response.get('Datapoints', []):
        avg += item.get('Average', 0)
    

    return "{0:.2f}".format(avg / tot_metrics)


def get_ec2_regions_list():
    ec2 = session.client('ec2')

    response = ec2.describe_regions()

    regions = []
    for region in response['Regions']:

        regions.append(region['RegionName'])

    return regions


def main(argv):

    global session

    ec2_infos = [['Region', 'AvailabilityZone', 'InstanceId', 'InstanceType', 'PrivateDnsName', 'PublicDnsName', 'Tags', 'State', '% CPU AVG']]
    regions = [argv.region] if argv.region != "" and argv.region != "all" else get_ec2_regions_list()
    last_days = argv.last_days

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

        for instance in response['Reservations']:

            current_instance_data = instance['Instances'][0]

            tags = []
            for tag in current_instance_data['Tags']:
                tags.append(f"{tag.get('Key')}: {tag.get('Value')}")

            cpu_avg = get_cpu_util(current_instance_data['InstanceId'], last_days)

            ec2_infos.append([  region, 
                                current_instance_data['Placement'].get('AvailabilityZone'), 
                                current_instance_data['InstanceId'],
                                current_instance_data['InstanceType'],
                                current_instance_data['PrivateDnsName'],
                                current_instance_data['PublicDnsName'] if current_instance_data['PublicDnsName'] != "" else current_instance_data['PublicIpAddress'],
                                ",".join(tags),
                                current_instance_data['State'].get('Name'),
                                cpu_avg,
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
    parser.add_argument('-d', '--days', dest='last_days', metavar='N', type=int, default=7, help='get CPU Util for x last days' )

    args = parser.parse_args()

    main(args)
