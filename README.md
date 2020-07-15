# python-aws-scripts

    Scripts to help get some informations about your infra in AWS

# Install dependecies
    pip install -r requirements.txt

# Configure AWS Credentials

    set up credentials (in e.g. ~/.aws/credentials):
    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET

# Run - Example ec2_list script
    Script to find EC2 in AWS
    You can filter by Region 
    You can choice returned data in a table or csv format
    Example of usage:

        python ec2_list.py 
        python ec2_list.py -o csv
        python ec2_list.py -r us-east-1
