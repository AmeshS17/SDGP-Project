import json
import urllib.parse
import boto3
import csv
import io

s3 = boto3.client('s3')

def get_json(bucket,key):
    
    json_object = s3.get_object(Bucket=bucket, Key=key)
    json_content = json_object['Body']
    
    json_dict = json.load(json_content)
    
    print(json_dict)
    print("Json dictionary length : " + str(len(json_dict)))
    
    return json_dict


def lambda_handler(event, context):
    
    print("Invocation event - " + str(event))

    # Get the object from the event and show its content type
    get_bucket = 'summary-json-files'

    get_key = event["queryStringParameters"]['filekey']
    
    try:
        summary = get_json(get_bucket,get_key)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(summary)
        }
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(get_key, get_bucket))
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({"filekey":get_key})
        }
        raise e


