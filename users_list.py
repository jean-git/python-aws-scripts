__author__ = "Jean Carlos Bezerra"
__maintainer__ = "Jean Carlos Bezerra"
__email__ = "jean2104@gmail.com"
__status__ = "Production"
"""
    Script to list IAM users in AWS
    You can choice returned data in a table or csv format
    Example of usage:
        python users_list.py 
        python users_list.py -o csv
"""
import datetime
import boto3
import sys, argparse
import json
from tabulate import tabulate

session = boto3.Session() # get default configurations of aws cli


def main(argv):

    global session

    iam = session.client('iam')

    users_infos = [['UserId', 'UserName', 'CreateDate', 'PasswordLastUsed', 'Groups', 'TotalAccessKeys', 'Tags']]

    response = iam.list_users()

    print(f"Total found: {len(response['Users'])}")

    for user in response['Users']:
        
        user_groups = []
        for group in iam.list_groups_for_user(UserName=user['UserName'])['Groups']:
            user_groups.append(group.get('GroupName'))

        total_access_keys = len(iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata'])

        tags = []
        for tag in iam.list_user_tags(UserName=user['UserName'])['Tags']:
            tags.append(f"{tag.get('Key')}: {tag.get('Value')}")

        users_infos.append([user.get('UserId'), 
                            user.get('UserName'), 
                            user.get('CreateDate'),
                            user.get('PasswordLastUsed'),
                            ",".join(user_groups),
                            total_access_keys,
                            ",".join(tags),
                            ])


    if argv.output == 'csv':
        for user in users_infos:
            print(','.join(user))
    else:
        print(tabulate(users_infos,
                headers="firstrow", tablefmt="grid")
                )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='IAM Users List options')
    parser.add_argument('-o', '--output', dest='output', metavar='csv', default='table', choices=['table', 'csv'], help='type of return, csv or table' )

    args = parser.parse_args()

    main(args)
