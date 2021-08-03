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
            "node_id": self.nid,
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
        for i, node in enumerate(self.nodes):
            print(f'node {node.nid}, index {i}')
        for i, link in enumerate(self.links):
            print(f'links {link.source} {link.target}, index {i}')

    def collapseNode(self):
        """Gets rid of extra nrange(lenodes and links"""
        delNodes = []
        delLinks = []

        for node in self.nodes:
            if node.value == -2:
                # ideally. there should be one source
                linkArrSrc = [
                    x for x in self.links if x.target == node.nid]
                if len(linkArrSrc) == 1:
                    linkArrSrc = linkArrSrc[0]

                linkArrTrgt = [
                    x for x in self.links if x.source == node.nid]

                delLinks.append(linkArrSrc)

                for i, _ in enumerate(linkArrTrgt):
                    self.links.append(
                        Links(linkArrSrc.source, linkArrTrgt[i].target, linkArrTrgt[i].count))
                    delLinks.append(linkArrTrgt[i])

                delNodes.append(node)

        #print(f'Node delete {[node. nid for node in delNodes]}')
        # print(
        #    f'Link delete {[((link.source, link.target)) for link in delLinks]}')

        # print(self.printGraph())

        delNodeIndices = [self.nodes.index(x) for x in delNodes]
        delLinkIndices = [self.links.index(x) for x in delLinks]

        #print(f'Node delete {delNodeIndices}')
        #print(f'Link delete {delLinkIndices}')

        for idx in sorted(delNodeIndices, reverse=True):
            del self.nodes[idx]

        for idx in sorted(delLinkIndices, reverse=True):
            del self.links[idx]
