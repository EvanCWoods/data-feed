import time
import requests
from pymongo import MongoClient
import ssl
import sys
import os

# GLOBAL VARIABLES
HOUR = 10
API_ENDPOINT = os.getenv('API_ENDPOINT')

cluster = MongoClient(os.getenv("MONGO_URI"),
ssl_cert_reqs=ssl.CERT_NONE)
db = cluster["data"]
collection = db.live

# Function to get the data from the api
def getDataFeed(API_ENDPOINT):
    data = requests.get(API_ENDPOINT)
    data = data.json()
    return data["USD"]


# Recursive function to get the current unix timestamp
def getHours():

    currentTime = int(time.time())  # Get the current time as an interger

    if (currentTime % HOUR == 0):   # If the time is devisable by the number of seconds in an hour, it is a new hour
        collection.insert_one({
            "timestamp": int(time.time()),
            "Close": getDataFeed(API_ENDPOINT) 
        })
        time.sleep(1)
        getHours()
    else:   # If the current time is not a new hour, re run the function, adding a 1 second delay
        time.sleep(1)
        getHours()

def main():
    getHours()
    sys.exit(1)


if __name__=="__main__":
    main()
    sys.exit(1)