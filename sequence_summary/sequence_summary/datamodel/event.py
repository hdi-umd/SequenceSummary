"""Implements the base class Event and it's derivative classes Point and Interval."""


class Event:
    """Base Event class that holds event types and attributes.

    This is the abstract base class for all event types in the system.
    Events can be extended to support different temporal characteristics
    (e.g., point events that occur at a specific moment, interval events
    that span a period).

    Attributes:
        type (str): The type of event ('point' or 'interval')
        attributes (dict): Dictionary of event attributes and their values
    """

    def __init__(self, eventtype):
        self.type = eventtype
        self.attributes = {}

    def addAttribute(self, attr, value):
        """Add attributes to the Event object."""
        self.attributes[attr] = value

    def getAttrVal(self, attrName):
        """Return Attribute value given attribute name."""
        return self.attributes.get(attrName, None)


class PointEvent(Event):
    """Derivative class for Point events"""

    def __init__(self, timestamp):
        Event.__init__(self, "point")
        # self.type = "point"
        self.timestamp = timestamp


class IntervalEvent(Event):
    """Derivative class for interval events."""

    def __init__(self, t1, t2):
        Event.__init__(self, "interval")
        # self.type = "interval"
        self.time = [t1, t2]
