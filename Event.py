class Event:
    def __init__(self, eventtype, attributes):
        self.type = eventtype
        self.attributes = attributes

    # Return Attribute value given attribute name
    def getAttrVal(self, attrName):
        return self.attributes.get(attrName, None)


# A class that represents a point event
class PointEvent(Event):
    def __init__(self, timestamp, attributes):
        Event.__init__(self, "point", attributes)
        #self.type = "point"
        self.timestamp = timestamp
        # dictionary: key=attribute value=attribute value


# class to represent an interval event
class IntervalEvent(Event):
    def __init__(self, t1, t2, attributes):
        Event.__init__(self, "interval", attributes)
        #self.type = "interval"
        self.time = [t1, t2]
        # dictionary: key=attribute value=attribute value
