import time
import requests
from pymongo import MongoClient
import os
import sys

# GLOBAL VARIABLES
HOUR = 3600
API_ENDPOINT="https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"

try:
    client = MongoClient(os.environ["MONGO_URI"])
    db = client["myDatabase"]
    collection = db["live-data"]
except:
    sys.exit(1)

# Function to get the data from the api
def getDataFeed(API_ENDPOINT):
    data = requests.get(API_ENDPOINT)
    data = data.json()
    return data["USD"]


# Recursive function to get the current unix timestamp
def getHours():
    currentTime = int(time.time())  # Get the current time as an interger
    if (currentTime % HOUR == 0):   # If the time is devisable by the number of seconds in an hour, it is a new hour
        collection.insert_one(
            {
                "USD": getDataFeed(API_ENDPOINT),
                "Timestamp": currentTime
            }
        )
        time.sleep(1)
        getHours()
    else:   # If the current time is not a new hour, re run the function, adding a 1 second delay
        time.sleep(1)
        getHours()

def main():
    getHours()


if __name__=="__main__":
    main()