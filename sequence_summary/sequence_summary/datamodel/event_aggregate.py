"""Aggregating events that have similar properties if there is a large number of event types."""

import re


def giveDictionaryOfMappingsFile(fileName):
    """Helper function to run the mappings file as a dictionary."""

    # Open the file and split the contents on new lines
    file = open(fileName, "r")
    mappings = file.read().split("\n")
    file.close()
    # Remove any empty strings from the list of mappings
    mappings = list(filter(None, mappings))
    # Raise an error if there is an odd number of items in mapping
    if (len(mappings) % 2) != 0:
        raise ValueError("There must be an even number of lines in the mappings file.")
    # Create a dictionary based on read in mappings
    aggregations = {}
    for i, _ in enumerate(mappings):
        if i % 2 == 0:
            aggregations[mappings[i]] = mappings[i + 1]
    return aggregations


# NOTE: this current modifies the events in eventList argument
# merge events by rules expressed in regular expressions.
# For example, in the highway incident dataset, we can
# replace all events with the pattern “CHART Unit [number]
# departed” by “CHART Unit departed”. The argument
# regexMapping can be a path pointing to a file defining such rules.
#  We can assume each rule occupies two lines:
# first line is the regular expression, second line is the merged event name


def aggregateEventsRegex(eventStore, regexMapping, attributeName):
    """This function modifies the events in eventList argument
    merge events by rules expressed in regular expressions.
    The argument regexMapping can be a path pointing to a file defining such rules.
    We can assume each rule occupies two lines:
    first line is the regular expression, second line is the merged event name
    """

    aggregations = giveDictionaryOfMappingsFile(regexMapping)
    eventList = eventStore.events
    for event in eventList:
        # Get the attribute value of interest
        attributeVal = event.attributes[attributeName]
        # For all the regexes
        for regex in aggregations:
            # If its a match then replace the attribute value for event with
            if re.match(regex, attributeVal):
                event.attributes[attributeName] = aggregations[regex]
                break
    eventStore.createAttrDict()
    return eventList


# NOTE: this current modifies the events in eventList argument
# merge events by a dictionary mapping an event name to the merged name.
# The argument nameDict can be a path
# pointing to a file defining such a dictionary.
# We can assume each mapping occupies two lines: first line is the
# original name, second line is the merged event name.


def aggregateEventsDict(eventStore, nameDict, attributeName):
    """this current modifies the events in eventList argument
    # merge events by a dictionary mapping an event name to the merged name.
    # The argument nameDict can be a path
    # pointing to a file defining such a dictionary.
    # We can assume each mapping occupies two lines: first line is the
    # original name, second line is the merged event name.
    """

    aggregations = giveDictionaryOfMappingsFile(nameDict)
    # Iterate over all events and replace evevnts in event list with updated attribute name
    # if directed to by given mappings
    eventList = eventStore.events
    for event in eventList:
        # Get the attribute value of interest
        attributeVal = event.attributes[attributeName]
        # If the attribute value has a mapping then replace the event's current value with the
        # one in given map
        if attributeVal in aggregations:

            event.attributes[attributeName] = aggregations[attributeVal]
    eventStore.createAttrDict()
    return eventList
