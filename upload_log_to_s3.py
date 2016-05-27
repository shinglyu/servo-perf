import argparse
import json
import tinys3

DEFAULT_BUCKET = 'servo-perf'
# DEFAULT_ENDPOINT = 's3-us-west-2.amazonaws.com'


def upload_to_s3(filename, remote_filename):

    with open('credential.json', 'r') as f:
        cred = json.load(f)

    conn = tinys3.Connection(cred['S3_ACCESS_KEY'],
                             cred['S3_SECRET_KEY'],
                             tls=True)
                             # endpoint=DEFAULT_ENDPOINT)

    f = open(filename, 'rb')
    conn.upload(remote_filename, f, DEFAULT_BUCKET)

if __name__ == '__main__':
    from os.path import basename

    parser = argparse.ArgumentParser(
        description="Upload a file to S3. The credential needs to be stored in credential.json. Default bucket: servo-perf"
    )
    parser.add_argument("path",
                        help="the file you want to upload")
    args = parser.parse_args()
    upload_to_s3(args.path, basename(args.path))
