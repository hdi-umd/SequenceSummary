from Event import IntervalEvent
from Sequence import Sequence
import pandas as pd
import requests
import os

# Helper function to return a data frame
# Local is boolean, if local then source should be path to the file
# Otherwise it should be a URL to the the file
def get_dataframe( src, local=False, sep="\t", header=[]):
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
        #else use header param for column names
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

# Split a long sequence into shorter ones by timeUnit. For example, a sequence may span several days and we want to 
# break it down into daily sequences. The argument timeUnit can be one of the following strings: “hour”, “day”, 
# “week”, “month”, “quarter”, and “year”.
# For interval events I used the start time of the event to determine its category when splitting it

#ZINAT- changes
#SequenceList represents a list of objects of type Sequence. The sequences are further splitted into
#sequence objects, this way we can use generate sequences and then splitSequences 
@staticmethod
def splitSequences(sequenceLists, timeUnit, record=None):
    if not isinstance(sequenceLists, list):
        sequenceLists=[sequenceLists]
    eventstore=sequenceLists[0].eventstore
    results = []
    resultlist=[]
    timeUnit = timeUnit.lower()
    # Check if the time unit is a valid argument
    valid_time_units = ["hour", "day", "week", "month", "quarter", "year"]
    if timeUnit not in valid_time_units:
        raise ValueError("timeUnit must be hour, day, week, month, quarter, or year")
    
    for sequence in sequenceLists:
        # Sort the events by the timestamp or event start time
        sequenceList= sequence.events
        sequenceList = sorted(sequenceList, key=get_time_to_sort_by)

        # Process the event sequence based on the given time unit
        # Generally, create a map for that time unit and then add each event into that map 
        # (key=time such as May 2021 in case of month, value=sequence) and then return the values of the map as a list
        if timeUnit == "hour":
            hours = {}
            for event in sequenceList:
                time = get_time_to_sort_by(event)
                key = (time.hour, time.day, time.month, time.year)
                insert_event_into_dict(key,hours,event)
                if record is None:
                    event.attributes["record"]=' '.join([str(k) for k in key])
                else:
                    event.attributes[record]=str(event.attributes[record])+"_"+' '.join([str(k) for k in key])
            results = list(hours.values())

        elif timeUnit == "day":
            days = {}
            for event in sequenceList:
                time = get_time_to_sort_by(event)
                key = (time.day, time.month, time.year)
                insert_event_into_dict(key,days,event)
                #print(days)
                if record is None:
                    event.attributes["record"]=datetime(*(key[::-1])).strftime("%Y%m%d")
                else:
                    event.attributes[record]=str(event.attributes[record])+"_"+datetime(*(key[::-1])).strftime("%Y%m%d")
            results = list(days.values())

        elif timeUnit == "month":
            months = {}
            for event in sequenceList:
                time = get_time_to_sort_by(event)
                key = (time.month,time.year)
                insert_event_into_dict(key,months,event)
                if record is None:
                    event.attributes["record"]=str(key[0])+str(key[1])
                else:
                    event.attributes[record]=str(event.attributes[record])+"_"+str(key[0])+str(key[1])
            results = list(months.values())

        elif timeUnit == "week":
            weeks = {}
            for event in sequenceList:
                time = get_time_to_sort_by(event)
                year = time.year
                week_num = time.isocalendar()[1]
                key = (year,week_num)
                insert_event_into_dict(key,weeks,event)
                if record is None:
                    event.attributes["record"]=str(key[0])+"W"+str(key[1])
                else:
                    event.attributes[record]=str(event.attributes[record])+"_"+str(key[0])+"W"+str(key[1])
            results = list(weeks.values())

        elif timeUnit == "year":
            years = {}
            for event in sequenceList:
                time = get_time_to_sort_by(event)
                key = time.year
                insert_event_into_dict(key,years,event)
                if record is None:
                    event.attributes["record"]=str(key)
                else:
                    event.attributes[record]=str(event.attributes[record])+"_"+str(key)
            results = list(years.values())

        elif timeUnit == "quarter":
            quarters = {}
            for event in sequenceList:
                time = get_time_to_sort_by(event)
                year = time.year
                month = time.month
                # Determine the year, quarter pair/key for quarter dict
                # January, February, and March (Q1)
                if month in range(1, 4):
                    key = (year, "Q1")
                # April, May, and June (Q2)
                elif month in range(4, 7):
                    key = (year, "Q2")
                # July, August, and September (Q3)
                elif month in range(7,10):
                    key = (year, "Q3")
                # October, November, and December (Q4)
                elif month in range(10,13):
                    key = (year, "Q4")
                # Put the event in the dictionary
                insert_event_into_dict(key,quarters,event)
                if record is None:
                    event.attributes["record"]=str(key[0])+str(key[1])
                else:
                    event.attributes[record]=str(event.attributes[record])+"_"+str(key[0])+str(key[1])
            results = list(quarters.values())
        resultlist.extend(results)
    resultlists= [Sequence(x, eventstore) for x in resultlist]

    return resultlists