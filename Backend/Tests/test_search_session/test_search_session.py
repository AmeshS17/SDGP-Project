import requests

def test_get_game_list(api_url):
    response = requests.get(api_url)
    assert response.status_code == 200
    print ('test_get_game_list passed')
    print(response.text)


base_url = 'https://8k7ni4cse1.execute-api.us-west-2.amazonaws.com/github-deploy-test/games'

test_get_game_list(base_url)
