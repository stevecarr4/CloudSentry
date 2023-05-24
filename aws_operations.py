import os
import boto3
from tabulate import tabulate
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='aws_script.log', filemode='w')
logger = logging.getLogger(__name__)

# Read AWS credentials from environment variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Initialize the AWS session
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-1'
)

# Create an EC2 client using the session
ec2_client = session.client('ec2')
s3_client = session.client('s3')

# Validate EC2 instance ID
def validate_instance_id(instance_id):
    pattern = r"^i-\w{8}$"  # Instance ID format: i- followed by 8 alphanumeric characters
    if re.match(pattern, instance_id):
        return instance_id
    else:
        raise ValueError("Invalid instance ID format.")

# Validate S3 bucket name
def validate_bucket_name(bucket_name):
    pattern = r"^[a-z0-9.-]{3,63}$"  # Bucket name format: lowercase alphanumeric characters, dots, and dashes
    if re.match(pattern, bucket_name):
        return bucket_name
    else:
        raise ValueError("Invalid bucket name format.")

# Example: Describe EC2 instances
def describe_instances():
    try:
        response = ec2_client.describe_instances()
        instances = response['Reservations']
        
        table_data = []
        for reservation in instances:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']
                table_data.append([instance_id, instance_type, state])
        
        if table_data:
            headers = ["Instance ID", "Instance Type", "State"]
            print(tabulate(table_data, headers, tablefmt="grid"))
        else:
            print("No instances found.")
        
        logging.info("Describe instances successful.")
    except Exception as e:
        logging.error(f"Error in describe_instances: {e}", extra={'input': ''})
        print("An error occurred while describing instances.")

# Example: Create an S3 bucket
def create_s3_bucket(bucket_name):
    try:
        # Check if the bucket already exists
        response = s3_client.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name in existing_buckets:
            print(f"Bucket '{bucket_name}' already exists.")
            return

        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': session.region_name
            },
        )
        print(f"Successfully created S3 bucket: {bucket_name}")
    except Exception as e:
        logging.error(f"Error creating S3 bucket: {e}", extra={'input': bucket_name})
        print(f"Error creating S3 bucket: {e}")

# Terminate an EC2 instance
def terminate_instance():
    instance_id = input("Enter the ID of the instance to terminate: ")
    try:
        # Check if the instance is in a state that allows termination
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if instance_state not in ['running', 'stopped']:
            print(f"Instance '{instance_id}' cannot be terminated in its current state: {instance_state}")
            return
        
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} termination request sent.")
    except Exception as e:
        logging.error(f"Error terminating instance: {e}", extra={'input': instance_id})
        print(f"Error terminating instance: {e}")

# Delete an S3 bucket
def delete_s3_bucket():
    bucket_name = input("Enter the name of the S3 bucket to delete: ")
    try:
        # Check if the bucket exists
        response = s3_client.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name not in existing_buckets:
            print(f"Bucket '{bucket_name}' does not exist.")
            return

        response = s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Successfully deleted S3 bucket: {bucket_name}")
    except Exception as e:
        logging.error(f"Error deleting S3 bucket: {e}", extra={'input': bucket_name})
        print(f"Error deleting S3 bucket: {e}")

# Launch a new EC2 instance
def launch_instance():
    instance_type = input("Enter the instance type: ")
    ami_id = input("Enter the AMI ID: ")
    key_name = input("Enter the key pair name: ")
    
    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Successfully launched EC2 instance: {instance_id}")
    except Exception as e:
        print(f"Error launching EC2 instance: {e}")

# Start an EC2 instance
def start_instance():
    instance_id = input("Enter the ID of the instance to start: ")
    
    try:
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} start request sent.")
    except Exception as e:
        print(f"Error starting instance: {e}")

# Stop an EC2 instance
def stop_instance():
    instance_id = input("Enter the ID of the instance to stop: ")
    
    try:
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} stop request sent.")
    except Exception as e:
        print(f"Error stopping instance: {e}")

# Create a Security Group
def create_security_group():
    group_name = input("Enter a name for the security group: ")
    description = input("Enter the description for the security group: ")
    
    try:
        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description=description
        )
        group_id = response['GroupId']
        print(f"Successfully created security group: {group_id}")
    except Exception as e:
        print(f"Error creating security group: {e}")

# Delete a Security Group
def delete_security_group():
    group_id = input("Enter the ID of the security group to delete: ")
    
    try:
        response = ec2_client.delete_security_group(GroupId=group_id)
        print(f"Successfully deleted security group: {group_id}")
    except Exception as e:
        print(f"Error deleting security group: {e}")

# Modify a Security Group
def modify_security_group():
    group_id = input("Enter the ID of the security group to modify: ")
    new_description = input("Enter the new description for the security group: ")
    
    try:
        response = ec2_client.modify_security_group_attributes(
            GroupId=group_id,
            Description=new_description
        )
        print(f"Successfully modified security group: {group_id}")
    except Exception as e:
        print(f"Error modifying security group: {e}")

# Upload a File to S3 Bucket
def upload_file():
    bucket_name = input("Enter the name of the S3 bucket: ")
    file_path = input("Enter the path to the file to upload: ")
    object_key = input("Enter the object key for the file: ")
    
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_key)
        print(f"Successfully uploaded file to S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Error uploading file to S3 bucket: {e}")

# Download a File from S3 Bucket
def download_file():
    bucket_name = input("Enter the name of the S3 bucket: ")
    object_key = input("Enter the object key of the file to download: ")
    file_path = input("Enter the path to save the downloaded file: ")
    
    try:
        response = s3_client.download_file(bucket_name, object_key, file_path)
        print(f"Successfully downloaded file from S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Error downloading file from S3 bucket: {e}")

# Create an EBS Snapshot
def create_snapshot():
    volume_id = input("Enter the ID of the EBS volume to create a snapshot: ")
    description = input("Enter the description for the snapshot: ")
    
    try:
        response = ec2_client.create_snapshot(
            VolumeId=volume_id,
            Description=description
        )
        snapshot_id = response['SnapshotId']
        print(f"Successfully created EBS snapshot: {snapshot_id}")
    except Exception as e:
        print(f"Error creating EBS snapshot: {e}")

# Restore an EBS snapshot
def restore_snapshot():
    snapshot_id = input("Enter the ID of the EBS snapshot to restore: ")
    availability_zone = input("Enter the availability zone for restoration: ")
    
    try:
        response = ec2_client.restore_snapshot(
            SnapshotId=snapshot_id,
            AvailabilityZone=availability_zone
        )
        print(f"Successfully initiated restoration of EBS snapshot: {snapshot_id}")
    except Exception as e:
        print(f"Error initiating restoration of EBS snapshot: {e}")

# Tag an EC2 instance
def tag_instance():
    instance_id = input("Enter the ID of the instance to tag: ")
    tag_key = input("Enter the tag key: ")
    tag_value = input("Enter the tag value: ")
    
    try:
        response = ec2_client.create_tags(
            Resources=[instance_id],
            Tags=[
                {
                    'Key': tag_key,
                    'Value': tag_value
                }
            ]
        )
        print(f"Successfully tagged instance: {instance_id}")
    except Exception as e:
        print(f"Error tagging instance: {e}")

# Tag an S3 bucket
def tag_bucket():
    bucket_name = input("Enter the name of the S3 bucket to tag: ")
    tag_key = input("Enter the tag key: ")
    tag_value = input("Enter the tag value: ")
    
    try:
        response = s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {
                        'Key': tag_key,
                        'Value': tag_value
                    }
                ]
            }
        )
        print(f"Successfully tagged S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Error tagging S3 bucket: {e}")
