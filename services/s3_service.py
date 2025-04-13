import boto3
from botocore.config import Config
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class S3Manager:
    def __init__(self):
        self._initialize_client()
        self.bucket = settings.S3_BUCKET

    def _initialize_client(self):
        """Initialize client with appropriate settings for local/production"""
        config = Config(
            signature_version='s3v4',
            s3={'addressing_style': 'path'}
        )
        
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL,  # Critical for MinIO
            config=config,
            region_name=settings.AWS_REGION
        )
    
    async def get_image_url(self, s3_key: str) -> str:
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': s3_key},
            ExpiresIn=3600
        )

    async def create_bucket_if_not_exists(self):
        try:
            self.client.create_bucket(Bucket=self.bucket)
        except self.client.exceptions.BucketAlreadyOwnedByYou:
            pass


s3_manager = S3Manager()
