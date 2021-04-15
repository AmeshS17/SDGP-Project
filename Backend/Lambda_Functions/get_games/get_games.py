import json

import boto3

from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('games')


def get_game_list(table):
    scan_kwargs = {
        'ProjectionExpression': "id, title, #description,filekey",
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
    response = get_game_list(table)
    for game in response:
        game_id = int(game['id'])
        update_dict = {"id":game_id}
        game.update(update_dict)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
