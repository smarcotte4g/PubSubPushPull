import os
import time
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import json
import pandas as pd
import datetime
from pandas.io.json import json_normalize

# GCP topic, project & subscription ids
PUB_SUB_PROJECT = "PROJECTNAME"
PUB_SUB_SUBSCRIPTION = "PROJECTNAME-sub"

## Google json key with 'Pub/Sub Publisher' and 'Pub/Sub Subscriber' permissions
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="FILE.json"

# Pub/Sub consumer timeout
timeout = 5.0

# callback function for processing consumed payloads 
# prints recieved payload
def process_payload(message):
    # get message data as a string
    string_json_data = message.data.decode('utf-8')
    # load into json object
    z = json.loads(string_json_data)
    # change timestamp from epoch to datetime
    z['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(z['timestamp']))

    # turn json object to data frame
    df = pd.json_normalize(z)
    # create payload csv unless exists otherwise append, add header if file is being created otherwise skip
    with open('pubsub_payload.csv', 'a') as f:
        df.to_csv(f, header=f.tell()==0, index=False, line_terminator='\n')
    # acknowledge the message
    message.ack()

# consumer function to consume messages from a topics for a given timeout period
def consume_payload(project, subscription, callback, period):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project, subscription)
        #print(f"Listening for messages on {subscription_path}..\n")
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        # Wrap subscriber in a 'with' block to automatically call close() when done.
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.                
                streaming_pull_future.result(timeout=period)
            except TimeoutError:
                streaming_pull_future.cancel()


# loop to test producer and consumer functions with a 3 second delay
while(True):    
    #print("===================================")
    consume_payload(PUB_SUB_PROJECT, PUB_SUB_SUBSCRIPTION, process_payload, timeout)
    #time.sleep(3)