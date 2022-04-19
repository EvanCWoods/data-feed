import time
import requests
from pymongo import MongoClient
import ssl
from decouple import config

# GLOBAL VARIABLES
HOUR = 1
API_ENDPOINT="https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"

    # value = str(os.environ["MONGO_URI"])
    # print(value)

# Function to get the data from the api
def getDataFeed(API_ENDPOINT):
    data = requests.get(API_ENDPOINT)
    data = data.json()
    return data["USD"]


# Recursive function to get the current unix timestamp
def getHours():
    cluster = MongoClient(config["MONGO_URI"],
    ssl_cert_reqs=ssl.CERT_NONE)
    db = cluster["test"]
    collection = db.test

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


if __name__=="__main__":
    main()