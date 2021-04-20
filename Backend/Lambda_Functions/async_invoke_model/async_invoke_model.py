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
    
    key = event["queryStringParameters"]['filekey'][:-4]+"csv"
    
    invoke_model(key)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps({"Message":'Model successfully invoked'})
    }
