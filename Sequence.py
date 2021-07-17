# collection of events sharing similar property

from itertools import count
from Event import Event
from helper import get_dataframe, get_time_to_sort_by, insert_event_into_dict
from datetime import datetime, timedelta


class Sequence():
    _ids = count(0)

    def __init__(self,  eventlist, eventstore, sid=None):
        # sequence id
        if sid is None:
            self.sid = next(self._ids)
        else:
            self.sid = sid

        self.events = eventlist
        self.eventstore = eventstore
        self.volume = 1
        self.seqAttributes = {}
        self.seqIndices = []

    def getEventPosition(self, attr, hash_val):
        for count, event in enumerate(self.events):
            # if event.getAttrVal(attr)==hash_val:
            if self.eventstore.attrdict[attr][event.getAttrVal(attr)] == hash_val:
                return count
        return -1

    def setVolume(self, intValue):
        self.volume = intValue

    def getVolume(self):
        return self.volume

    def increaseVolume(self):
        self.volume += 1

    def getUniqueValueHashes(self, attr):
        l = list(set(event.getAttrVal(attr) for event in self.events))
        uniquelist = [self.eventstore.attrdict[attr][elem] for elem in l]
        return uniquelist

    # Not sure this will always result in same index, will change if
    #dictionary is updated
    # since python is unordered

    def getHashList(self, attr):
        #l=list(list(event.attributes.keys()).index(attr) for event in self.events)
        l = [event.getAttrVal(attr) for event in self.events]
        hashlist = [self.eventstore.attrdict[attr][elem] for elem in l]

        return hashlist

    def getValueHashes(self, attr):
        l = list(event.getAttrVal(attr) for event in self.events)
        hashlist = [self.eventstore.attrdict[attr][elem] for elem in l]

        return hashlist

    def getEventsHashString(self, attr):
        s = attr+": "
        l = list(event.getAttrVal(attr) for event in self.events)
        # for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" "
        s += "".join(str(self.eventstore.attrdict[attr][elem]) for elem in l)
        return s

    def convertToVMSPReadablenum(self, attr):
        l = list(event.getAttrVal(attr) for event in self.events)
        s = " -1 ".join(str(self.eventstore.attrdict[attr][elem])
                        for elem in l)
        # s=""
        # for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" -1 "
        s += " -2"

        return s

    def convertToVMSPReadable(self, attr):
        l = list(event.getAttrVal(attr) for event in self.events)
        s = " ".join(self.eventstore.attrdict[attr][elem] for elem in l)
        # s=""
        # for count,event in enumerate(self.events):
        #    s+=str(event.getAttrVal(attr))+" -1 "
        s += "."

        return s

    def getPathID(self):
        return self.sid

    def matchPathAttribute(self, attr, val):
        # should i use eq?!
        if self.seqAttributes.get(attr) == (val):
            return True
        else:
            return False

    def setSequenceAttribute(self, attr, value):
        self.seqAttributes[attr] = value

    # equivalent to method signature public static int getVolume(List<Sequence> seqs)

    def getSeqVolume(seqlist):
        return sum(seq.getVolume() for seq in seqlist)

    # Method equivalent to public String getEvtAttrValue(String attr, int hash) in DataManager.java

    def getEvtAttrValue(self, attr, hashval):
        return self.eventstore.reverseatttrdict[attr][hashval]

    # Method equivalent to public List<String> getEvtAttrValues(String attr) in DataManager.java
    def getEvtAttrValues(self, attr):
        return list(self.eventstore.reverseatttrdict[attr].values())

    # Method equivalent to int getEvtAttrValueCount(String attr) in DataManager.java
    def getEvtAttrValueCount(self, attr):
        return len(self.eventstore.reverseatttrdict[attr])

    # Split a long sequence into shorter ones by timeUnit. For example, a sequence may span several days and we want to
    # break it down into daily sequences. The argument timeUnit can be one of the following strings: “hour”, “day”,
    # “week”, “month”, “quarter”, and “year”.
    # For interval events I used the start time of the event to determine its category when splitting it

    #ZINAT- changes
    # SequenceList represents a list of objects of type Sequence. The sequences are further splitted into
    # sequence objects, this way we can use generate sequences and then splitSequences
    @staticmethod
    def splitSequences(sequenceLists, timeUnit, record=None):
        if not isinstance(sequenceLists, list):
            sequenceLists = [sequenceLists]
        eventstore = sequenceLists[0].eventstore
        results = []
        resultlist = []
        timeUnit = timeUnit.lower()
        # Check if the time unit is a valid argument
        valid_time_units = ["hour", "day", "week", "month", "quarter", "year"]
        if timeUnit not in valid_time_units:
            raise ValueError(
                "timeUnit must be hour, day, week, month, quarter, or year")

        for sequence in sequenceLists:
            # Sort the events by the timestamp or event start time
            sequenceList = sequence.events
            sequenceList = sorted(sequenceList, key=get_time_to_sort_by)

            # Process the event sequence based on the given time unit
            # Generally, create a map for that time unit and then add each event into that map
            # (key=time such as May 2021 in case of month, value=sequence) and then return the values of the map as a list
            if timeUnit == "hour":
                hours = {}
                for event in sequenceList:
                    time = get_time_to_sort_by(event)
                    key = (time.hour, time.day, time.month, time.year)
                    insert_event_into_dict(key, hours, event)
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
                    time = get_time_to_sort_by(event)
                    key = (time.day, time.month, time.year)
                    insert_event_into_dict(key, days, event)
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
                    time = get_time_to_sort_by(event)
                    key = (time.month, time.year)
                    insert_event_into_dict(key, months, event)
                    if record is None:
                        event.attributes["record"] = str(key[0])+str(key[1])
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+str(key[0])+str(key[1])
                results = list(months.values())

            elif timeUnit == "week":
                weeks = {}
                for event in sequenceList:
                    time = get_time_to_sort_by(event)
                    year = time.year
                    week_num = time.isocalendar()[1]
                    key = (year, week_num)
                    insert_event_into_dict(key, weeks, event)
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
                    time = get_time_to_sort_by(event)
                    key = time.year
                    insert_event_into_dict(key, years, event)
                    if record is None:
                        event.attributes["record"] = str(key)
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+str(key)
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
                    elif month in range(7, 10):
                        key = (year, "Q3")
                    # October, November, and December (Q4)
                    elif month in range(10, 13):
                        key = (year, "Q4")
                    # Put the event in the dictionary
                    insert_event_into_dict(key, quarters, event)
                    if record is None:
                        event.attributes["record"] = str(key[0])+str(key[1])
                    else:
                        event.attributes[record] = str(
                            event.attributes[record])+"_"+str(key[0])+str(key[1])
                results = list(quarters.values())
            resultlist.extend(results)
        resultlists = [Sequence(x, eventstore) for x in resultlist]

        return resultlists
