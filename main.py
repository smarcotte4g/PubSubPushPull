import json
import requests
from bs4 import BeautifulSoup as bs
import hashlib
import os
import time
from pathlib import Path
import urllib.request
from google.cloud import pubsub_v1

CURRENT_VERSION = 0.1
INSTALL_LOC = 'C:\\LOCATION_OF_FILES\\'

# GCP topic, project & subscription ids
PUB_SUB_TOPIC = "CREATED-topic"
PUB_SUB_PROJECT = "GCP_PROJECT_NAME"

## Google json key with 'Pub/Sub Publisher' and 'Pub/Sub Subscriber' permissions
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="learn-321620-e313efc6a715.json"

def main():
    check_all_hash()
    
    # can use this to get the md5hash of file to add to required.json
    #print(hashlib.md5(open(INSTALL_LOC + 'ui_auction.inc','rb').read()).hexdigest())
    
    # playing around with
    #web_ver = get_web_version()

def check_all_hash():
    # open the required.json file
    with open("required.json") as r:
        # load
        data = json.load(r)
        # count how many lines
        count_req = len(data)
        # variable to hold increment
        total_percent = 0
        # divide to get increment
        percentage_of = 100/count_req
        # loop through each item
        for r_data in data:
            # get file_location and replace / with \\
            file_location = INSTALL_LOC + r_data['name'].replace('/', '\\')
            # so we can use is_file
            item = Path(file_location)
            # check to see if it is a file
            if item.is_file():
                # get the actual md5 of the file
                downloaded_hash = hashlib.md5(open(file_location,'rb').read()).hexdigest()
                # check it agaist the json md5
                if downloaded_hash == r_data['md5']:
                    pass
                # md5 do not match
                else:
                    print('Hash do not match! Deleting and downloading new file: ' + r_data['name'])
                    # Removed the file because it is not correct anyway
                    os.remove(file_location)

                    # Download the correct file
                    urllib.request.urlretrieve(r_data['url'], file_location)
            # file does not exists
            else:
                # Get the file path of what json is showing
                path_location = os.path.dirname(os.path.abspath(file_location))
                # if it is a directory
                if os.path.isdir(path_location):
                    # download the new file from the url
                    print('File does not exist! Downloading: ' + r_data['name'])
                    urllib.request.urlretrieve(r_data['url'], file_location)
                # it is not a directory
                else:
                    # create the directory
                    os.makedirs(path_location, exist_ok=True)
                    # download the new file from the url
                    print('File does not exist! Downloading: ' + r_data['name'])
                    urllib.request.urlretrieve(r_data['url'], file_location)
            # create a payload to send to pubsub
            payload = {"data" : r_data['name'] + " MD5Sum Correct", "timestamp": time.time()}
            print(f"Sending payload: {payload}.")
            # push the payload
            push_payload(payload, PUB_SUB_TOPIC, PUB_SUB_PROJECT)
            # increment and output the percent complete
            total_percent += percentage_of
            print(str(round(total_percent)) + '/100')
            
    return

# producer function to push a message to a topic
def push_payload(payload, topic, project):
        # create the publisher
        publisher = pubsub_v1.PublisherClient()
        # create the topic path
        topic_path = publisher.topic_path(project, topic)
        # get the payload as a json object
        data = json.dumps(payload).encode("utf-8")
        # push
        future = publisher.publish(topic_path, data=data)
        print("Pushed message to topic.")

def get_web_version():
    # a url to just a txt with version number
    url = 'https://raw.githubusercontent.com/main/version.txt'
    response = requests.get(url)
    ver_from_web = bs(response.content,features="html.parser")
    # strip the contents and just get the version number
    ver_from_web = check_version(ver_from_web.text.strip())
    return ver_from_web


def check_version(web_ver):
    is_current = True
    f = open("version.json", "r")
    v_data = json.load(f)
    if (v_data["version"] != CURRENT_VERSION) and (web_ver != CURRENT_VERSION):
        is_current = False
        return is_current
    return is_current

def get_location():
    cwd = os.getcwd()
    return cwd


if __name__=="__main__":
    main()