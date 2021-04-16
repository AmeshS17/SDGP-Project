import requests
import time


def get_upload_url(api_url):
    response = requests.get(api_url+"upload-url")
    print("get_upload_url response = " + str(response.json()))
    assert response.status_code == 200
    print ('get_upload_url passed')
    return response.json()


def upload_file(upload_url,file_path):
    with open(file_path,"rb") as file:
        response = requests.put(upload_url,data=file)
    print( "upload_file response status" + str(response.status_code))
    assert response.status_code == 200
    print ('upload_file passed')
    print(file.name + " has been uploaded to S3")


def get_summary(base_url,file_key):
    payload = {"filekey":file_key}
    for i in range(6):
        response = requests.post(base_url+"results",json=payload)
        print("get_summary request {} response = ".format(i) + str(response.json()))
        assert response.status_code == 200
        lambda_status_code = int(response.json()['statusCode'])
        if lambda_status_code == 204:
            time.sleep((i+1)*5)
            continue
        if lambda_status_code == 200:
            print ('get_summary passed')
            return response.json()
    #Raise an exception if results were not returned after 6 tries
    raise Exception("Results were not returned after requesting 6 times")
    

base_url = 'https://8k7ni4cse1.execute-api.us-west-2.amazonaws.com/github-deploy-test/'



upload_url_response = get_upload_url(base_url) 
upload_url = upload_url_response['uploadurl']
file_key = upload_url_response['filekey']

file_path = "./Backend/Tests/test_upload_session/testfile.csv"

upload_file(upload_url,file_path)
summary_response = get_summary(base_url,file_key)
