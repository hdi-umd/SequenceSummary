from datetime import datetime, timedelta
from Event import PointEvent, IntervalEvent
from Sequence import Sequence
from helper import get_dataframe, get_time_to_sort_by, insert_event_into_dict


class EventStore:

    def __init__(self, eventlist=[]):
        self.attrdict = {}
        self.reverseatttrdict = {}
        self.events = eventlist

    # should be moved to EventStore
    # hold the list of events, also the dictionaries

    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # header is list of column names if they are not provided in the dataset
    # The foursquare datasets are all using a differnet encoding that pandas cannot auto identify so for those
    # I thought the simplest thing was just to give this function the df and then use that instead of calling my helper
    # for those cases
    # @staticmethod
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
        self.events = events
        # sequence=Sequence(events)
        self.create_attr_dict()
        # return sequence

    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # The foursquare datasets are all using a differnet encoding that pandas cannot auto identify so for those
    # I thought the simplest thing was just to give this function the df and then use that instead of calling my helper
    # for those cases
    # @staticmethod
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
        self.events = events
        # sequence=Sequence(events)
        self.create_attr_dict()
        # return sequence

    # Import a dataset that has both interval and point events
    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # The foursquare datasets are all using a differnet encoding that pandas cannot auto identify so for those
    # I thought the simplest thing was just to give this function the df and then use that instead of calling my helper
    # @staticmethod
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
            # list of indices to be ignored
            ignore = [startTimeColumnIdx, endTimeColumnIdx]
            attribute_columns = [ind for ind in range(
                len(data)) if ind not in ignore]
            for i in attribute_columns:
                attribs[cols[i]] = data[i]
            # use time stamp (or t1 and t2) and attributes map to construct event object
            if event_type == "point":
                e = PointEvent(t, attribs)
            else:
                e = IntervalEvent(t1, t2, attribs)
            events.append(e)
        self.events = events
        # sequence=Sequence(events)
        self.create_attr_dict()
        # return sequence

    # should take an eventlist as input
    # Group events by attributeName, and order them by timestamp
    # @staticmethod
    # should return a list of sequences
    def generateSequence(self, attributeName):
        eventList = self.events
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
        sequences = list(grouped_by.values())
        seqlist = []
        for seq in sequences:
            seqlist.append(Sequence(seq, self))
        return seqlist

    def getUniqueValues(self, attr):
        l = list(set(event.getAttrVal(attr) for event in self.events))
        return l

    # Assuming we are given a list of events and from those events we create
    # the mapping and reverse mapping dictionary
    def create_attr_dict(self):
        attr_list = self.events[0].attributes.keys()
        print(attr_list)

        for attr in attr_list:
            a = 48
            unique_list = []
            unique_list.extend(self.getUniqueValues(attr))
            unique_list = list(set(unique_list))
            # unique_list.clear()

            unicode_dict = {}
            reverse_dict = {}
            for uniques in unique_list:
                unicode_dict[uniques] = chr(a)
                reverse_dict[chr(a)] = uniques
                a = a+1
            self.attrdict[attr] = unicode_dict
            self.reverseatttrdict[attr] = reverse_dict
            # unicode_dict.clear()
