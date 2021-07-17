from Event import IntervalEvent
import pandas as pd
import requests
import os
from datetime import datetime, timedelta

# Helper function to return a data frame
# Local is boolean, if local then source should be path to the file
# Otherwise it should be a URL to the the file


def get_dataframe(src, local=False, sep="\t", header=[]):
    if not local:
        # To force a dropbox link to download change the dl=0 to 1
        if "dropbox" in src:
            src = src.replace('dl=0', 'dl=1')
        # Download the CSV at url
        req = requests.get(src)
        url_content = req.content
        csv_file = open('data.txt', 'wb')
        csv_file.write(url_content)
        csv_file.close()
        # Read the CSV into pandas
        # If header list is empty, the dataset provides header so ignore param
        if not header:
            df = pd.read_csv("data.txt", sep)
        # else use header param for column names
        else:
            df = pd.read_csv("data.txt", sep, names=header)
        # Delete the csv file
        os.remove("data.txt")
        return df
    # Dataset is local
    else:
        # If header list is empty, the dataset provides header so ignore param
        if not header:
            print(src)
            df = pd.read_csv(src, sep)
        # else use header param for column names
        else:
            df = pd.read_csv(src, sep, names=header)
        return df


# Helper function for generateSequence to use when sorting events to get what time field to sort by
# Also used in splitSequences to give the time of an event when splitting the events up

def get_time_to_sort_by(e):
    # Sort by starting time of event if its an interval event
    if type(e) == IntervalEvent:
        return e.time[0]
    # Otherwise use the timestamp
    else:
        return e.timestamp


# Helper to insert an event into a map
# Params are key=unique id for that time, map of key to event list, event object
def insert_event_into_dict(key, dictionary, event):
    if key in dictionary:
        dictionary[key].append(event)
    else:
        dictionary[key] = [event]
