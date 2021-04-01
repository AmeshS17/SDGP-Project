import json

import boto3

from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('games')

def get_game(id, table):
    try:
        response = table.get_item(Key={'id': id})
    except ClientError as e:
        return e.response['Error']['Message']
    else:
        return response.get('Item',"No items found")


def get_game_list(table):
    scan_kwargs = {
        'ProjectionExpression': "id, title, #description",
        'ExpressionAttributeNames': {"#description": "desc"}
    }

    games_list = []

    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        games_list.extend(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
        
    return games_list


def lambda_handler(event, context):
    if event['queryStringParameters'] and 'id' in event['queryStringParameters']:
        game_id = int(event['queryStringParameters']['id'])
        response = get_game(game_id, table)
        
        if 'title' in response:
            return {
                'statusCode': 200,
                'body': json.dumps('Requested game found: ' + response['title'])
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
    else:
        response = get_game_list(table)
        single_game_id = int(response[0]['id'])
        for game in response:
            game_id = int(game['id'])
            update_dict = {"id":game_id}
            game.update(update_dict)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
