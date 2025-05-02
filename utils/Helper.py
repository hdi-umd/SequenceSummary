"""Defines various helper functions to create EventStore object from given source."""

import os
import pandas as pd
import requests
from datamodel.Event import IntervalEvent


def getDataframe(src, local=False, sep="\t", header=None):
    """Helper function to return a data frame
    Local is boolean, if local then source should be path to the file
    Otherwise it should be a URL to the the file
    """

    if not local:
        # To force a dropbox link to download change the dl=0 to 1
        if "dropbox" in src:
            src = src.replace("dl=0", "dl=1")
        # Download the CSV at url
        req = requests.get(src)
        urlContent = req.content
        csvFile = open("data.txt", "wb")
        csvFile.write(urlContent)
        csvFile.close()
        # Read the CSV into pandas
        # If header list is empty, the dataset provides header so ignore param
        if header is None:
            dataFrame = pd.read_csv("data.txt", sep)
        # else use header param for column names
        else:
            dataFrame = pd.read_csv("data.txt", sep, names=header)
        # Delete the csv file
        os.remove("data.txt")
        # return dataFrame
    # Dataset is local
    else:
        # If header list is empty, the dataset provides header so ignore param
        if not header:
            # print(src)
            dataFrame = pd.read_csv(src, sep=sep)
        # else use header param for column names
        else:
            dataFrame = pd.read_csv(src, sep=sep, names=header)
    return dataFrame


def getTimeToSortBy(evt):
    """Helper function for generateSequence to use when sorting events to get
    what time field to sort by. Also used in splitSequences to give the time of
    an event when splitting the events up
    """

    # Sort by starting time of event if its an interval event
    if isinstance(evt, IntervalEvent):
        return evt.time[0]
    # Otherwise use the timestamp
    return evt.timestamp


def insertEventIntoDict(key, dictionary, event):
    """Helper to insert an event into a map Params are key=unique id for that time,
    map of key to event list, event object
    """
    if key in dictionary:
        dictionary[key].append(event)
    else:
        dictionary[key] = [event]
