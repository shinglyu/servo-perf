import argparse
import json
import boto3
from boto3.s3.transfer import S3Transfer


DEFAULT_BUCKET = 'servo-perf'
# DEFAULT_ENDPOINT = 's3-us-west-2.amazonaws.com'


def upload_to_s3(filename, remote_filename):

    with open('credential.json', 'r') as f:
        cred = json.load(f)

    client = boto3.client('s3',
                          aws_access_key_id=cred['S3_ACCESS_KEY'],
                          aws_secret_access_key=cred['S3_SECRET_KEY'])
    transfer = S3Transfer(client)
    transfer.upload_file(filename, DEFAULT_BUCKET, remote_filename)


if __name__ == '__main__':
    from os.path import basename

    parser = argparse.ArgumentParser(
        description="Upload a file to S3. The credential needs to be stored in credential.json. Default bucket: servo-perf"
    )
    parser.add_argument("path",
                        help="the file you want to upload")
    args = parser.parse_args()
    upload_to_s3(args.path, basename(args.path))
