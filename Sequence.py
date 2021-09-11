"""Module implements the Sequence class with associated functions."""

from itertools import count
#from Event import Event
from datetime import datetime
from Helper import getTimeToSortBy, insertEventIntoDict


class Sequence():
    """Collection of events sharing similar property."""

    _ids = count(0)

    def __init__(self, eventlist, eventstore, sid=None):
        # sequence id
        if sid is None:
            self._id = next(self._ids)
        else:
            self._id = sid
        self.sid = self
        self.events = eventlist
        self.eventstore = eventstore
        self.volume = 1
        self.seqAttributes = {}
        self.seqIndices = []

    def getSeqLen(self):
        """"Length of the eventList for this sequence."""
        print(f'event Length {self.events}')
        return len(self.events)

    def getEventPosition(self, attr, hashVal):
        """Returns the position of first event where the value of attr matches the
        given hash value.
        """
        for pos, event in enumerate(self.events):
            # if event.getAttrVal(attr)==hashVal:
            if self.eventstore.attrDict[attr][event.getAttrVal(attr)] == hashVal:
                return pos
        return -1

    def setVolume(self, intValue):
        """Assigns the volume value to intValue."""
        self.volume = intValue

    def getVolume(self):
        """Returns the volume value for this object."""
        return self.volume

    def increaseVolume(self):
        """Increases volume value by 1."""
        self.volume += 1

    def getUniqueValueHashes(self, attr):
        """Returns Hash values for unique attribute types for the specified attribute
         in the dictionary
         """
        lst = list(set(event.getAttrVal(attr) for event in self.events))
        uniquelist = [self.eventstore.attrDict[attr][elem] for elem in lst]
        return uniquelist

    # Not sure this will always result in same index, will change if
    #dictionary is updated
    # since python is unordered

    def getHashList(self, attr):
        """"Returns a list of index positions of the specified attribute for all
        the events  in the sequence
        """
        #lst=list(list(event.attributes.keys()).index(attr) for event in self.events)
        lst = [event.getAttrVal(attr) for event in self.events]
        hashlist = [self.eventstore.attrDict[attr][elem] for elem in lst]

        return hashlist

    def getValueHashes(self, attr):
        """Returns a list of values of the specified attribute for all the
        events in the sequence
        """
        lst = list(event.getAttrVal(attr) for event in self.events)
        hashlist = [self.eventstore.attrDict[attr][elem] for elem in lst]

        return hashlist

    def getEventsHashString(self, attr):
        """Returns a string containing a list of values of the specified attribute
        for all the events in the sequence
        """
        string = attr + ": "
        lst = list(event.getAttrVal(attr) for event in self.events)
        # for count,event in enumerate(self.events):
        #    string+=str(event.getAttrVal(attr))+" "
        string += "".join(str(self.eventstore.attrDict[attr][elem])
                          for elem in lst)
        return string

    def convertToVMSPReadablenum(self, attr):
        """Returns a VMSP readable string of numbers containing a list of values of
        the specified attribute for all the events in the sequence
        """
        lst = list(event.getAttrVal(attr) for event in self.events)
        string = " -1 ".join(str(self.eventstore.attrDict[attr][elem])
                             for elem in lst)
        # string=""
        # for count,event in enumerate(self.events):
        #    string+=str(event.getAttrVal(attr))+" -1 "
        string += " -2"

        return string

    def convertToVMSPReadable(self, attr):
        """Returns a VMSP readable string containing a list of values of
        the specified attribute for all the events in the sequence
        """
        lst = list(event.getAttrVal(attr) for event in self.events)
        string = " ".join(self.eventstore.attrDict[attr][elem] for elem in lst)
        # string=""
        # for count,event in enumerate(self.events):
        #    string+=str(event.getAttrVal(attr))+" -1 "
        string += "."

        return string

    def getPathID(self):
        """Returns the sequence ID value for this object."""
        return self.sid

    def matchPathAttribute(self, attr, val):
        """Returns True if the value for specified sequence attribute matches the specified value"""
        # should i use eq?!
        return bool(self.seqAttributes.get(attr) == (val))

    def setSequenceAttribute(self, attr, value):
        """Assigns the value of the specified attribute to the specified Value"""
        self.seqAttributes[attr] = value

    # equivalent to method signature public static int getVolume(List<Sequence> seqs)
    @staticmethod
    def getSeqVolume(seqlist):
        """Return aggregated value of total volume of all the sequences
        in the given List of Sequences.
        """
        return sum(seq.getVolume() for seq in seqlist)

    @staticmethod
    def getUniqueEvents(seqlist, attr):
        """Get all possible event types"""
        # return self.eventstore.reverseAttrDict[attr].values()
        return list(set(event.getAttrVal(attr) for event in seq for seq in seqlist))

    # Method equivalent to public String getEvtAttrValue(String attr, int hash) in DataManager.java

    def getEvtAttrValue(self, attr, hashVal):
        """Given hashVal, return original value for the specified attr"""
        return self.eventstore.reverseAttrDict[attr][hashVal]

    # Method equivalent to public List<String> getEvtAttrValues(String attr) in DataManager.java
    def getEvtAttrValues(self, attr):
        """Given attr name, return all possible values for that attribute"""
        return [event.getAttrVal(attr) for event in self.events]

    # Method equivalent to int getEvtAttrValueCount(String attr) in DataManager.java
    def getEvtAttrValueCount(self, attr):
        """return the number of distinct types present given an attribute"""
        return len(self.eventstore.reverseAttrDict[attr])

    def getEventsString(self, attr):
        """Convert the sequence events to a string."""
        return "\t".join(elem for elem in self.getEvtAttrValues(attr))

    #ZINAT- changes
    # SequenceList represents a list of objects of type Sequence.
    # The sequences are further splitted into
    # sequence objects, this way we can use generate sequences and then splitSequences
    @staticmethod
    def splitSequences(sequenceLists, timeUnit, record=None):
        """Split a long sequence into shorter ones by timeUnit. For example, a sequence
        may span several days and we want to break it down into daily sequences. The argument
        timeUnit can be one of the following strings: “hour”, “day”, “week”, “month”, “quarter”,
        and “year”. For interval events the start time of the event  is used to determine its
        category when splitting it
        """
        if not isinstance(sequenceLists, list):
            sequenceLists = [sequenceLists]
        eventstore = sequenceLists[0].eventstore
        results = []
        resultlist = []
        timeUnit = timeUnit.lower()
        # Check if the time unit is a valid argument
        validTimeUnits = ["hour", "day", "week", "month", "quarter", "year"]
        if timeUnit not in validTimeUnits:
            raise ValueError(
                "timeUnit must be hour, day, week, month, quarter, or year")

        for sequence in sequenceLists:
            # Sort the events by the timestamp or event start time
            sequenceList = sequence.events
            sequenceList = sorted(sequenceList, key=getTimeToSortBy)

            # Process the event sequence based on the given time unit
            # Generally, create a map for that time unit and then add each event into that map
            # (key=time such as May 2021 in case of month, value=sequence) and then return the
            # values of the map as a list
            if timeUnit == "hour":
                hours = {}
                for event in sequenceList:
                    time = getTimeToSortBy(event)
                    key = (time.hour, time.day, time.month, time.year)
                    insertEventIntoDict(key, hours, event)
                    if record is None:
                        event.attributes["record"] = ' '.join(
                            [str(k) for k in key])
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+' '.join([str(k) for k in key])
                results = list(hours.values())

            elif timeUnit == "day":
                days = {}
                for event in sequenceList:
                    time = getTimeToSortBy(event)
                    key = (time.day, time.month, time.year)
                    insertEventIntoDict(key, days, event)
                    # print(days)
                    if record is None:
                        event.attributes["record"] = datetime(
                            *(key[::-1])).strftime("%Y%m%d")
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+datetime(*(key[::-1])).strftime("%Y%m%d")
                results = list(days.values())

            elif timeUnit == "month":
                months = {}
                for event in sequenceList:
                    time = getTimeToSortBy(event)
                    key = (time.month, time.year)
                    insertEventIntoDict(key, months, event)
                    if record is None:
                        event.attributes["record"] = str(key[0])+str(key[1])
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+str(key[0])+str(key[1])
                results = list(months.values())

            elif timeUnit == "week":
                weeks = {}
                for event in sequenceList:
                    time = getTimeToSortBy(event)
                    year = time.year
                    weekNum = time.isocalendar()[1]
                    key = (year, weekNum)
                    insertEventIntoDict(key, weeks, event)
                    if record is None:
                        event.attributes["record"] = str(
                            key[0])+"W"+str(key[1])
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+str(key[0])+"W"+str(key[1])
                results = list(weeks.values())

            elif timeUnit == "year":
                years = {}
                for event in sequenceList:
                    time = getTimeToSortBy(event)
                    key = time.year
                    insertEventIntoDict(key, years, event)
                    if record is None:
                        event.attributes["record"] = str(key)
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+str(key)
                results = list(years.values())

            elif timeUnit == "quarter":
                quarters = {}
                for event in sequenceList:
                    time = getTimeToSortBy(event)
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
                    elif month in range(7, 10):
                        key = (year, "Q3")
                    # October, November, and December (Q4)
                    elif month in range(10, 13):
                        key = (year, "Q4")
                    # Put the event in the dictionary
                    insertEventIntoDict(key, quarters, event)
                    if record is None:
                        event.attributes["record"] = str(key[0])+str(key[1])
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+str(key[0])+str(key[1])
                results = list(quarters.values())
            resultlist.extend(results)
        resultlists = [Sequence(x, eventstore) for x in resultlist]

        return resultlists
