import unittest
from aws_operations import describe_instances, create_s3_bucket, terminate_instance, delete_s3_bucket
from moto import mock_ec2, mock_s3
import boto3

class TestAwsOperations(unittest.TestCase):
    def setUp(self):
        self.region = 'us-east-1'
        boto3.setup_default_session(region_name=self.region)

    @mock_ec2
    def test_describe_instances(self):
        ec2_client = boto3.client('ec2')
        instances = ec2_client.run_instances(ImageId='ami-12345678', MinCount=1, MaxCount=1)['Instances']

        instances = describe_instances()
        self.assertTrue(len(instances) > 0, "Expected non-empty list of instances")

        ec2_client.terminate_instances(InstanceIds=[instance['InstanceId'] for instance in instances])
        instances = describe_instances()
        self.assertEqual(len(instances), 0, "Expected empty list of instances")

    @mock_s3
    def test_create_s3_bucket(self):
        s3_client = boto3.client('s3')

        bucket_name = "my-test-bucket"
        create_s3_bucket(bucket_name)

        response = s3_client.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
        self.assertIn(bucket_name, existing_buckets, "Bucket creation failed")

        invalid_bucket_name = "invalid_bucket_name"
        with self.assertRaises(ValueError):
            create_s3_bucket(invalid_bucket_name)
        
        if bucket_name in existing_buckets:
            delete_s3_bucket(bucket_name)

    @mock_ec2
    def test_terminate_instance(self):
        ec2_client = boto3.client('ec2')
        instances = ec2_client.run_instances(ImageId='ami-12345678', MinCount=1, MaxCount=1)['Instances']
        instance_id = instances[0]['InstanceId']

        terminate_instance(instance_id)

        instances = describe_instances()
        self.assertEqual(len(instances), 0, "Instance termination failed")

        invalid_instance_id = "invalid_instance_id"
        with self.assertRaises(ValueError):
            terminate_instance(invalid_instance_id)

    @mock_s3
    def test_delete_s3_bucket(self):
        s3_client = boto3.client('s3')
        bucket_name = "my-test-bucket"
        create_s3_bucket(bucket_name)
        
        delete_s3_bucket(bucket_name)

        response = s3_client.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
        self.assertNotIn(bucket_name, existing_buckets, "Bucket deletion failed")

        invalid_bucket_name = "invalid_bucket_name"
        with self.assertRaises(ValueError):
            delete_s3_bucket(invalid_bucket_name)


if __name__ == '__main__':
    unittest.main()
