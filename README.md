# python-aws-scripts

    Scripts to help get some informations about your infra in AWS

# Install dependecies
    pip install -r requirements.txt

# Run
    Script to find EC2 in AWS
    You can filter by Region 
    You can choice returned data in a table or csv format
    Example of usage:

        python ec2_list.py 
        python ec2_list.py -o csv
        python ec2_list.py -r us-east-1
