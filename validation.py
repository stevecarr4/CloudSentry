import re

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
