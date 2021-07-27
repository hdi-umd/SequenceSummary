""" Creates the RawNode, Links and Graph class."""

import json


class RawNode:
    """RawNode contains selected attributes from Node class for json conversion."""

    def __init__(self, node):
        self.nid = node.nid
        self.seqCount = node.seqCount
        self.value = node.value
        self.pattern = node.getPatternString()
        self.meanStep = node.meanStep
        self.medianStep = node.medianStep

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class RawNode."""
        return {
            "node id": self.nid,
            "event_attribute": self.value,
            "Pattern": self.pattern,
            "value": self.seqCount,
            "median_index": self.medianStep,
            "average_index": self.meanStep
        }


class Links:
    """Links class contains information regarding which node is connected to which one"""

    def __init__(self, node1, node2, count):
        self.source = node1
        self.target = node2
        self.count = count

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class Links."""
        return {
            "source": self.source,
            "target": self.target,
            "count": self.count
        }


class Graph:
    """Graph class consusts of Links and Nodes."""

    def __init__(self):
        self.links = []  # defaultdict(set)
        self.nodes = []

    # def add(self, node1, node2, count):
    #    self.links.append(Links(node1,node2, count))
        # self.links[node2].add(node1)

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class Graph."""
        return {
            "nodes": self.nodes,
            "links": self.links

        }

    def jsonSerialize(self) -> None:
        """Default JSON serializer"""
        json.dumps(self, indent=4, default=Graph.jsonSerializeDump)

    @staticmethod
    def jsonSerializeDump(obj):
        """static method to call jsonDefaultDump on all custom objects"""
        if hasattr(obj, "jsonDefaultDump"):

            return obj.jsonDefaultDump()
        if isinstance(obj, set):
            return list(obj)
        return None  # obj.__dict__

    def printGraph(self):
        """Print the node ids."""
        for node in self.nodes:
            print(node.nid)
