import json
import urllib.parse
import boto3
import csv
import io



s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

def get_csv(bucket,key):
    
    csv_object = s3.get_object(Bucket=bucket, Key=key)
    csv_content = csv_object['Body'].read().decode('utf-8').split('\n')
    
    csv_dict = list(csv.DictReader(csv_content))
    
    for row in csv_dict:
        author_playtime_forever = int(row['author.playtime_forever'])
        steam_purchase = row['steam_purchase'].lower() == 'true'
        received_for_free = row['received_for_free'].lower() == 'true'
        written_during_early_access = row['written_during_early_access'].lower() == 'true'
        update_dict = {"author.playtime_forever":author_playtime_forever,
                        "steam_purchase":steam_purchase,
                        "received_for_free":received_for_free,
                        "written_during_early_access":written_during_early_access}
        row.update(update_dict)


    print(csv_dict[:15])
    print("Data dictionary length : " + str(len(csv_dict)))
    
    return csv_dict


def put_csv(csv_dict,bucket,key):
    
    csv_object = filestream.getvalue()
    

    response = s3.put_object(Body=csv_object,Bucket=bucket,Key=key)

    print(response)
    return True


def invoke_model(key):
    response = lambda_client.invoke(
        FunctionName = 'generate_summary',
        InvocationType = 'Event',
        Payload = json.dumps({'filekey':key})
    )


def lambda_handler(event, context):

    print("Invocation event - " + str(event))

    # Get the object from the event and show its content type
    get_bucket = event['Records'][0]['s3']['bucket']['name']
    put_bucket = 'cleaned-csv-files'
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    waiter = s3.get_waiter('object_exists')
    waiter.wait(
        Bucket=get_bucket,
        Key=key,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts':15
        }
    )
    
    try:
        data_dict = get_csv(get_bucket,key)
        filestream = io.StringIO()



        uploaded = put_csv(filestream,put_bucket,key)
        
        waiter.wait(
        Bucket=put_bucket,
        Key=key,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts':15
            }
        )
    
        invoke_model(key)
        return None
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, get_bucket))
        raise e


