import json
import boto3

class AWSService:
    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key = secret_key

    def create_client(self, service_name: str):
        return boto3.client(
            service_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

class S3Service():
    def __init__(self, aws_service: AWSService, bucket_name: str):
        self.client = aws_service.create_client('s3')
        self.bucket_name = bucket_name

    def upload(self, local_path: str, remote_path: str):
        self.client.upload_file(local_path, self.bucket_name, remote_path)

    def download(self, remote_path: str, local_path: str):
        self.client.download_file(self.bucket_name, remote_path, local_path)

    def list_files(self, directory: str):
        response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=directory)
        return [obj['Key'] for obj in response.get('Contents', [])]

    def list_buckets(self):
        response = self.client.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]

class LambdaService:
    def __init__(self, aws_service: AWSService):
        self.client = aws_service.create_client('lambda')

    def invoke(self, function_name: str, payload: dict):
        response = self.client.invoke(FunctionName=function_name, Payload=json.dumps(payload))
        return response['Payload'].read().decode()

class EC2Service:
    def __init__(self, aws_service: AWSService):
        self.client = aws_service.create_client('ec2')

    def start_instance(self, instance_id: str):
        self.client.start_instances(InstanceIds=[instance_id])

    def stop_instance(self, instance_id: str):
        self.client.stop_instances(InstanceIds=[instance_id])

    def list_instances(self):
        response = self.client.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])
        return instances

class SQSService:
    def __init__(self, aws_service: AWSService):
        self.client = aws_service.create_client('sqs')

    def send_message(self, queue_url: str, message_body: str):
        self.client.send_message(QueueUrl=queue_url, MessageBody=message_body)

    def receive_message(self, queue_url: str):
        response = self.client.receive_message(QueueUrl=queue_url)
        return response.get('Messages', [])

class SNSService:
    def __init__(self, aws_service: AWSService):
        self.client = aws_service.create_client('sns')

    def publish_message(self, topic_arn: str, message: str):
        self.client.publish(TopicArn=topic_arn, Message=message)

    def list_topics(self):
        response = self.client.list_topics()
        return [topic['TopicArn'] for topic in response.get('Topics', [])]

class AWSCloud(AWSService):
    def __init__(self, access_key: str, secret_key: str):
        super().__init__(access_key, secret_key)

    def S3Service(self, bucket_name: str):
        return S3Service(self, bucket_name)

    def LambdaService(self):
        return LambdaService(self)

    def EC2Service(self):
        return EC2Service(self)

    def SQSService(self):
        return SQSService(self)

    def SNSService(self):
        return SNSService(self)
