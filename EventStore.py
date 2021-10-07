"""Implements the EventStore class to store events and attributes."""


from datetime import datetime
from Event import PointEvent, IntervalEvent
from Sequence import Sequence
from Helper import getDataframe, getTimeToSortBy


class EventStore:
    """EventStore class holds all tevents present in the dataset. Also creates a
    dictionary of event attribute to unicode mapping and the reverse mapping.
    """

    def __init__(self, eventlist=None):
        if eventlist is None:
            eventlist = []
        self.attrDict = {}
        self.reverseAttrDict = {}
        self.events = eventlist

    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # header is list of column names if they are not provided in the dataset
    # The foursquare datasets are all using a differnet encoding that pandas cannot
    #  auto identify so for those
    # I thought the simplest thing was just to give this function the dataFrame and
    # then use that instead of calling my helper
    # for those cases

    def importPointEvents(self, src, timeStampColumnIdx, timeFormat,
                          sep='\t', local=False, header=None, dataFrame=None):
        """ Returns a list of event objects
        src is a url or directory path, if local is false its url else its path
        header is list of column names if they are not provided in the dataset.
        """
        events = []
        # if the dataFrame is not provided
        if dataFrame is None:
            dataFrame = getDataframe(src, local, sep, header)
        cols = dataFrame.columns
        # For each event in the csv construct an event object
        for row in dataFrame.iterrows():
            data = row[1]
            try:
                timeStamp = datetime.strptime(data[timeStampColumnIdx], timeFormat)
            except ValueError:
                timeStamp = datetime.fromisoformat(data[timeStampColumnIdx])
            # for all attributes other tahn time, add them to attributes dict
            evt = PointEvent(timeStamp)
            for i, _ in enumerate(data):
                if i != timeStampColumnIdx:
                    evt.addAttribute(cols[i], data[i])
            # use time stamp and attributes map to construct event object
            events.append(evt)
        self.events = events
        # sequence=Sequence(events)
        self.createAttrDict()
        # return sequence

    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # The foursquare datasets are all using a differnet encoding that pandas
    # cannot auto identify so for those
    # I thought the simplest thing was just to give this function
    # the dataFrame and then use that instead of calling my helper
    # for those cases

    def importIntervalEvents(self, src, startTimeColumnIdx, endTimeColumnIdx,
                             timeFormat, sep="\t", local=False, header=None, dataFrame=None):
        """Returns a list of event objects
        src is a url or directory path, if local is false its url else its path.
        """
        events = []
        # if the dataFrame is not provided
        if dataFrame is None:
            dataFrame = getDataframe(src, local, sep, header)
        cols = dataFrame.columns
        # For each event in the csv construct an event object
        for row in dataFrame.iterrows():
            data = row[1]
            # create datetime object for the start and end times of the event
            try:
                timeStamp1 = datetime.strptime(
                    data[startTimeColumnIdx], timeFormat)
            except ValueError:
                timeStamp1 = datetime.fromisoformat(data[startTimeColumnIdx])

            try:
                timeStamp2 = datetime.strptime(data[endTimeColumnIdx], timeFormat)
            except ValueError:
                timeStamp2 = datetime.fromisoformat(data[endTimeColumnIdx])
            # for all attributes other than times, add them to attributes dict
            evt = IntervalEvent(timeStamp1, timeStamp2)
            for i, _ in enumerate(data):
                if i not in (startTimeColumnIdx, endTimeColumnIdx):
                    evt.addAttribute(cols[i], data[i])
                    #attribs[cols[i]] = data[i]
            # use time stamp and attributes map to construct event object
            events.append(evt)
        self.events = events
        # sequence=Sequence(events)
        self.createAttrDict()
        # return sequence

    # Import a dataset that has both interval and point events
    # Returns a list of event objects
    # src is a url or directory path, if local is false its url else its path
    # The foursquare datasets are all using a differnet encoding that pandas
    # cannot auto identify so for those
    # I thought the simplest thing was just to give this function the dataFrame and then
    # use that instead of calling my helper

    def importMixedEvents(self, src, startTimeColumnIdx, endTimeColumnIdx,
                          timeFormat, sep="\t", local=False, header=None, dataFrame=None):
        """Import a dataset that has both interval and point events
        Returns a list of event objects
        src is a url or directory path, if local is false its url else its path.
        """
        events = []
        # if the dataFrame is not provided
        if dataFrame is None:
            dataFrame = getDataframe(src, local, sep, header)
        cols = dataFrame.columns
        # For each event in the csv construct an event object
        for row in dataFrame.iterrows():
            data = row[1]
            # create datetime object for timeStamp (if point events)
            # or t1 and t2 (if interval event)
            # If the endTimeColumnIdx value is NaN ie a float instead of a time
            # string then its a point event
            # if isinstance(data[endTimeColumnIdx], float):
            if data[endTimeColumnIdx] is None or isinstance(data[endTimeColumnIdx], float):
                try:
                    timeStamp = datetime.strptime(
                        data[startTimeColumnIdx], timeFormat)
                except ValueError:
                    timeStamp = datetime.fromisoformat(data[startTimeColumnIdx])
                eventType = "point"
            # Otherwise its an interval event
            else:
                try:
                    timeStamp1 = datetime.strptime(
                        data[startTimeColumnIdx], timeFormat)
                except ValueError:
                    timeStamp1 = datetime.fromisoformat(data[startTimeColumnIdx])
                try:
                    timeStamp2 = datetime.strptime(
                        data[endTimeColumnIdx], timeFormat)
                except ValueError:
                    timeStamp2 = datetime.fromisoformat(data[endTimeColumnIdx])
                eventType = "interval"
            # for all attributes other than times, add them to attributes dict
            # list of indices to be ignored
            ignore = [startTimeColumnIdx, endTimeColumnIdx]
            attributeColumns = [ind for ind in range(
                len(data)) if ind not in ignore]
            if eventType == "point":
                evt = PointEvent(timeStamp)
            else:
                evt = IntervalEvent(timeStamp1, timeStamp2)
            for i in attributeColumns:
                evt.addAttribute(cols[i], data[i])
                #attribs[cols[i]] = data[i]
            # use time stamp (or t1 and t2) and attributes map to construct event object
            events.append(evt)
        self.events = events
        # sequence=Sequence(events)
        self.createAttrDict()
        # return sequence

    def generateSequence(self, attributeName):
        """Group events by attributeName, and order them by timestamp
        returns a list of sequences.
        """
        eventList = self.events
        groupedBy = {}
        # Sort the event list
        eventList = sorted(eventList, key=getTimeToSortBy)
        for event in eventList:
            value = event.attributes[attributeName]
            # If have seen this value before, append it the list of events in groupedBy for value
            if value in groupedBy:
                groupedBy[value].append(event)
            # otherwise store a new list with just that event
            else:
                groupedBy[value] = [event]
        sequences = list(groupedBy.values())
        seqlist = []
        for seq in sequences:
            seqlist.append(Sequence(seq, self))
        return seqlist

    def getUniqueValues(self, attr):
        """returns the unique values of a certain attribute
         present in the dataset.
         """
        uniqVals = list(set(event.getAttrVal(attr) for event in self.events))
        return uniqVals

    def getEventValue(self, attr, hashlist):
        """Given a list of hash values, return the original value of event."""
        return [self.reverseAttrDict[attr][val] for val in hashlist]

        # Method equivalent to int getEvtAttrValueCount(String attr) in DataManager.java
    def getEvtAttrValueCount(self, attr):
        """return the number of distinct types present given an attribute"""
        return len(self.reverseAttrDict[attr])

    # Method equivalent to public String getEvtAttrValue(String attr, int hash) in DataManager.java
    def getEvtAttrValue(self, attr, hashVal):
        """Given hashVal, return original value for the specified attr"""
        return self.reverseAttrDict[attr][hashVal]

    def createAttrDict(self):
        """ Assuming we are given a list of events and from those events we create
        the mapping and reverse mapping dictionary.
        """
        attrList = self.events[0].attributes.keys()
        #print(attrList)

        for attr in attrList:
            unicode = 48
            uniqueList = []
            uniqueList.extend(self.getUniqueValues(attr))
            uniqueList = list(set(uniqueList))
            # uniqueList.clear()

            unicodeDict = {}
            reverseDict = {}
            for uniques in uniqueList:
                unicodeDict[uniques] = chr(unicode)
                reverseDict[chr(unicode)] = uniques
                unicode = unicode+1
            self.attrDict[attr] = unicodeDict
            self.reverseAttrDict[attr] = reverseDict
            # unicodeDict.clear()
