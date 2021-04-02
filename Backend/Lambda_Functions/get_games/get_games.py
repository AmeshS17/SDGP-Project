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


def decimal_to_int(item_dict):
    update_dict = {
        "id":int(item_dict['id']),
        "release_year":int(item_dict['release_year'])
    }

    item_dict.update(update_dict)

    for key in item_dict['pos_features']:
        item_dict['pos_features'].update({key:int(item_dict['pos_features'][key])})

    for key in item_dict['neg_features']:
        item_dict['neg_features'].update({key:int(item_dict['neg_features'][key])})


def lambda_handler(event, context):
    if event['queryStringParameters'] and 'id' in event['queryStringParameters']:
        game_id = int(event['queryStringParameters']['id'])
        response = get_game(game_id, table)
        
        if 'title' in response:
            response = convert_to_int()
            response.update(update_dict)
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
    else:
        response = get_game_list(table)
        for game in response:
            game_id = int(game['id'])
            update_dict = {"id":game_id}
            game.update(update_dict)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
