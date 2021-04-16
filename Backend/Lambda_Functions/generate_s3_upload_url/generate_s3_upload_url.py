import json
import boto3
import uuid
from botocore.client import Config


def lambda_handler(event, context):
    # TODO implement
    
    print("Invocation event - " + str(event))
    
    s3 = boto3.client('s3', 'us-west-2', config=Config(s3={'addressing_style': 'path'}))
    
    # Generate a random S3 key name
    upload_key = uuid.uuid4().hex+".csv"

    # Generate the presigned URL for put requests
    presigned_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': 'raw-csv-files',
            'Key': upload_key,
            'ACL':'public-read-write'
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps({"uploadurl": presigned_url,"filekey":upload_key[:-3]+"json"})
    }
