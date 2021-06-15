from datetime import datetime, timedelta
from helper import get_dataframe, get_time_to_sort_by, insert_event_into_dict
from Event import PointEvent, IntervalEvent
from Sequence import Sequence
class EventStore:
    
    def __init__(self, eventlist=[]):
        self.attrdict={}
        self.reverseatttrdict={}
        self.events=eventlist

    #should be moved to EventStore
    # hold the list of events, also the dictionaries
    
    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # header is list of column names if they are not provided in the dataset
    # The foursquare datasets are all using a differnet encoding that pandas cannot auto identify so for those
    # I thought the simplest thing was just to give this function the df and then use that instead of calling my helper
    # for those cases
    #@staticmethod
    def importPointEvents(self, src, timestampColumnIdx, timeFormat, sep='\t', local=False, header=[], df=None):
        events = []
        # if the df is not provided
        if df is None:
            df = get_dataframe(src, local, sep, header)
        cols = df.columns
        # For each event in the csv construct an event object
        for row in df.iterrows():
            data = row[1]
            attribs = {}
            timestamp = datetime.strptime(data[timestampColumnIdx], timeFormat)
            # for all attributes other tahn time, add them to attributes dict
            for i in range(len(data)):
                if i != timestampColumnIdx:
                    attribs[cols[i]] = data[i]
            # use time stamp and attributes map to construct event object
            e = PointEvent(timestamp, attribs)
            events.append(e)
        self.events=events
        #sequence=Sequence(events)
        self.create_attr_dict()
        #return sequence

    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # The foursquare datasets are all using a differnet encoding that pandas cannot auto identify so for those
    # I thought the simplest thing was just to give this function the df and then use that instead of calling my helper
    # for those cases
    #@staticmethod
    def importIntervalEvents(self, src, startTimeColumnIdx, endTimeColumnIdx, timeFormat, sep="\t", local=False, header=[], df=None):
        events = []
        # if the df is not provided
        if df is None:
            df = get_dataframe(src, local, sep, header)
        cols = df.columns
        # For each event in the csv construct an event object
        for row in df.iterrows():
            data = row[1]
            attribs = {}
            # create datetime object for the start and end times of the event
            t1 = datetime.strptime(data[startTimeColumnIdx], timeFormat)
            t2 = datetime.strptime(data[endTimeColumnIdx], timeFormat)
            # for all attributes other than times, add them to attributes dict
            for i in range(len(data)):
                if i != startTimeColumnIdx and i != endTimeColumnIdx:
                    attribs[cols[i]] = data[i]
            # use time stamp and attributes map to construct event object
            e = IntervalEvent(t1, t2, attribs)
            events.append(e)
        self.events=events    
        #sequence=Sequence(events)
        self.create_attr_dict()
        #return sequence

    # Import a dataset that has both interval and point events
    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # The foursquare datasets are all using a differnet encoding that pandas cannot auto identify so for those
    # I thought the simplest thing was just to give this function the df and then use that instead of calling my helper
    #@staticmethod
    def importMixedEvents(self, src, startTimeColumnIdx, endTimeColumnIdx, timeFormat, sep="\t", local=False, header=[], df=None):
        events = []
        # if the df is not provided
        if df is None:
            df = get_dataframe(src, local, sep, header)
        cols = df.columns
        # For each event in the csv construct an event object
        for row in df.iterrows():
            data = row[1]
            attribs = {}
            # create datetime object for timestamp (if point events) or t1 and t2 (if interval event)
            # If the endTimeColumnIdx value is NaN ie a float instead of a time string then its a point event
            if type(data[endTimeColumnIdx]) is float:
                t = datetime.strptime(data[startTimeColumnIdx], timeFormat)
                event_type = "point"
            # Otherwise its an interval event
            else:
                t1 = datetime.strptime(data[startTimeColumnIdx], timeFormat)
                t2 = datetime.strptime(data[endTimeColumnIdx], timeFormat)
                event_type = "interval"
            # for all attributes other than times, add them to attributes dict
            ignore=[startTimeColumnIdx, endTimeColumnIdx] # list of indices to be ignored
            attribute_columns = [ind for ind in range(len(data)) if ind not in ignore]
            for i in attribute_columns:
                attribs[cols[i]] = data[i]
            # use time stamp (or t1 and t2) and attributes map to construct event object
            if event_type == "point":
                e = PointEvent(t, attribs)
            else:
                e = IntervalEvent(t1, t2, attribs)
            events.append(e)
        self.events=events   
        #sequence=Sequence(events)
        self.create_attr_dict()
        #return sequence

    #should take an eventlist as input
    # Group events by attributeName, and order them by timestamp
    #@staticmethod
    #should return a list of sequences
    def generateSequence(self, attributeName):
        eventList=self.events
        grouped_by = {}
        # Sort the event list
        eventList = sorted(eventList, key=get_time_to_sort_by)
        for event in eventList:
            value = event.attributes[attributeName]
            # If have seen this value before, append it the list of events in grouped_by for value
            if value in grouped_by:
                grouped_by[value].append(event)
            # otherwise store a new list with just that event
            else:
                grouped_by[value] = [event]
        sequences= list(grouped_by.values())
        seqlist=[]
        for seq in sequences:
            seqlist.append(Sequence(seq, self))
        return seqlist
    
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
    
    def getUniqueValues(self, attr):
        l=list(set(event.getAttrVal(attr) for event in self.events))
        return l
    
    #Assuming we are given a list of events and from those events we create 
    #the mapping and reverse mapping dictionary
    def create_attr_dict(self):
        attr_list=self.events[0].attributes.keys()
        print(attr_list)
        
        for attr in attr_list:
            a=48
            unique_list=[]
            unique_list.extend(self.getUniqueValues(attr))
            unique_list=list(set(unique_list))
            #unique_list.clear()
            
            unicode_dict={}
            reverse_dict={}
            for uniques in unique_list:
                unicode_dict[uniques]=chr(a)
                reverse_dict[chr(a)]=uniques
                a=a+1
            self.attrdict[attr]=unicode_dict
            self.reverseatttrdict[attr]=reverse_dict
            #unicode_dict.clear()                    
   