from minio import Minio
from config import host, access_key, secret_key


s3client = Minio(host,
                 access_key=access_key,
                 secret_key=secret_key,
                 secure=False)
