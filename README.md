# python-aws-scripts

    Scripts to help get some informations about your infra in AWS

# Scripts
- ec2_list.py -> Script to list EC2 instances in AWS(a specific or in all regions)

    ```
    will return:
        | Region | AvailabilityZone | ImageId | InstanceId | InstanceType | PrivateDnsName | PublicDnsName | Tags | State |
    ```

- ec2_cpu_avg.py -> Script to list EC2 instances and get CPU AVG in AWS(a specific or in all regions), default is last 7 days
    ```
    will return:
        | Region | AvailabilityZone | InstanceId | InstanceType | PrivateDnsName | PublicDnsName | Tags | State | % CPU AVG |
    ```
- ebs_list.py -> Script to list EBS in AWS(a specific or in all regions)
    ```
    will return:
        | Region | AvailabilityZone | VolumeId | InstanceId | Size(GB) | Iops | VolumeType | State | Tags |
    ```
- users_list.py -> Script to list IAM users in AWS with groups, tags and count their access keys.
    ```
    will return:
        | UserId | UserName | CreateDate | PasswordLastUsed | Groups | TotalAccessKeys | Tags |
    ```

# Install dependecies
    pip install -r requirements.txt

# Configure AWS Credentials

    You need to set up your AWS security credentials before the sample code is able to connect to AWS. 
    - Make sure, AWS credentials are set in ~/.aws/credentials or exported variables in your enviremont:
        - Linux or macOS:
            - export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
            - export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY

        - Windows Command Prompt:
            - setx AWS_ACCESS_KEY_ID YOUR_AWS_ACCESS_KEY_ID
            - setx AWS_SECRET_ACCESS_KEY YOUR_AWS_SECRET_ACCESS_KEY
        
        - PowerShell
            - $Env:AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
            - $Env:AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
    
# Run - Example ec2_list script
    Script to find EC2 in AWS
    You can filter by Region 
    You can choice returned data in a table or csv format
    Example of usage:

        python ec2_list.py 
        python ec2_list.py -o csv
        python ec2_list.py -r us-east-1
