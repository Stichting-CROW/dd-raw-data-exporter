import os
import boto3
import botocore

def init_boto():
    session = boto3.session.Session()
    client = session.client('s3',
        config=botocore.config.Config(s3={'addressing_style': 'virtual'}), 
        region_name='ams3',
        endpoint_url='https://ams3.digitaloceanspaces.com',
        aws_access_key_id=os.getenv('SPACES_KEY'),
        aws_secret_access_key=os.getenv('SPACES_SECRET')
    )
    
    return client


def upload_to_spaces(zip_file_location):
    client = init_boto()

    key = zip_file_location.split("/")[-1]
    client.upload_file(
        Filename=zip_file_location,
        Bucket='dashboarddeelmobiliteit',
        Key=key
    )

    url = client.generate_presigned_url(ClientMethod='get_object',
                                    Params={'Bucket': 'dashboarddeelmobiliteit',
                                            'Key': key},
                                    ExpiresIn=3600 * 24)

    return url