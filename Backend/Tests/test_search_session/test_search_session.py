import requests
import time

def get_game_list(api_url):
    response = requests.get(api_url+"games")
    assert response.status_code == 200
    print ('get_game_list passed')
    print("get_game_list response = " + str(response.json()))
    return response.json()


def invoke_model(api_url,file_key):
    payload={'filekey':file_key}
    response = requests.get(api_url+"model?filekey="+file_key)
    assert response.status_code == 200
    print('invoke_model passed')
    print('invoke_model response = ' + str(response.json()))

def get_summary(api_url,file_key):
    for i in range(60):
        response = requests.get(api_url+"results?filekey="+file_key)
        lambda_status_code = int(response.status_code)
        if lambda_status_code == 204:
            time.sleep(5)
            continue
        if lambda_status_code == 200:
            print ('get_summary passed')
            print("get_summary request {} response = ".format(i) + str(response.json()))
            return response.json()
    #Raise an exception if results were not returned after 6 tries
    raise Exception("Results were not returned after requesting 6 times")



base_url = 'https://8k7ni4cse1.execute-api.us-west-2.amazonaws.com/github-deploy-test/'

game_list = get_game_list(base_url)
test_file_key = ""
for game in game_list:
    if game['id'] == 0:
        test_file_key = game['filekey']

invoke_model(base_url,test_file_key)
summary = get_summary(base_url,test_file_key)

        
