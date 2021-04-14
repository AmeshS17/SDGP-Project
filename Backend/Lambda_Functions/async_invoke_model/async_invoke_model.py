import json
import boto3

lambda_client = boto3.client('lambda')

def invoke_model(key):
    response = lambda_client.invoke(
        FunctionName = 'generate_summary',
        InvocationType = 'Event',
        Payload = json.dumps({'filekey':key})
    )

def lambda_handler(event, context):
    # TODO implement
    
    print("Invocation event - " + str(event))
    
    key = event['filekey'][:-4]+"csv"
    
    invoke_model(key)
    
    return {
        'statusCode': 200,
        'body': json.dumps({"Message":'Model successfully invoked'})
    }
