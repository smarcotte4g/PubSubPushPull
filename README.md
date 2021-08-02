# Why?

This project was created to test json and pubsub. Download a file and add a md5 to required.json file. It will then check the md5 from the required.json and the installed file. After it is completed with all the files given, it will send a pubsub json object to GCP and retrieve it. After it retrieves the json payload it will fix the date and add it to a csv.

# Instructions

git clone https://github.com/smarcotte4g/PubSubPushPull.git

pip install any dependencies missing
google-api-python-client
google-cloud-pubsub

Download any file and get the md5sum (line 25 main.py). Add it to required.json and repeat for as many as you want.

Update main.py with your GCP and json file

INSTALL_LOC = 'C:\\LOCATION_OF_FILES\\'
PUB_SUB_TOPIC = "CREATED-topic"
PUB_SUB_PROJECT = "GCP_PROJECT_NAME"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="FILE.json"

Update pubsubget.py with your GCP info

PUB_SUB_PROJECT = "PROJECTNAME"
PUB_SUB_SUBSCRIPTION = "PROJECTNAME-sub"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="FILE.json"

Setup a Service Account in GCP and add grant permissions for 'Pub/Sub Publisher' and 'Pub/Sub Subscriber'
Add Key button and add a new JSON key. This will download a file to you computer and add it to os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="FILE.json"

Create a Pub/Sub Topic and leave defaults. This will create a topic-sub subscription

Run 2 terminals, start 