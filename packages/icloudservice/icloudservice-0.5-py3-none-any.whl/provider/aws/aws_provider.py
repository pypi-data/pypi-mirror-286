from icloudservice.src.service.aws.aws_services import AWSService
from icloudservice.src.service.aws.aws_services import S3Service,LambdaService,EC2Service,SNSService,SQSService

class AWSCloud(AWSService):
    def __init__(self, access_key: str, secret_key: str):
        super().__init__(access_key,secret_key)
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