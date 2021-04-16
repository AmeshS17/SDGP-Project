import json
import urllib.parse
import boto3
import csv
import io

s3 = boto3.client('s3')

def get_csv(bucket,key):
    
    csv_object = s3.get_object(Bucket=bucket, Key=key)
    csv_content = csv_object['Body'].read().decode('utf-8').split('\n')
    
    csv_dict = list(csv.DictReader(csv_content))
    
    print(csv_dict[:15])
    print("Data dictionary length : " + str(len(csv_dict)))
    
    return csv_dict


def put_json(csv_dict,bucket,key):
    sample_dict = csv_dict[:5]
    
    response = s3.put_object(Body=json.dumps(sample_dict).encode('utf-8'),Bucket=bucket,Key=key)

    print(response)
    return True


def lambda_handler(event, context):

    print("Invocation event - " + str(event))

    # Get the object from the event and show its content type
    get_bucket = 'cleaned-csv-files'
    put_bucket = 'summary-json-files'
    get_key = event['filekey']
    
    waiter = s3.get_waiter('object_exists')
    waiter.wait(
        Bucket=get_bucket,
        Key=get_key,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts':15
        }
    )
    
    try:
        data_dict = get_csv(get_bucket,get_key)
        
        
        put_key = get_key[:-3] + 'json'
        uploaded = put_json(data_dict,put_bucket,put_key)
        
        waiter.wait(
        Bucket=put_bucket,
        Key=put_key,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts':15
        }
    )
        
        return None
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(get_key, get_bucket))
        raise e


