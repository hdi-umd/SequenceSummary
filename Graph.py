""" Creates the RawNode, Links and Graph class."""

import json


class RawNode:
    """RawNode contains selected attributes from Node class for json conversion."""

    def __init__(self, node, pos = -1):
        self.nid = node.nid
        self.seqCount = node.seqCount
        self.value = node.value
        self.pattern = node.getPatternString()
        self.meanStep = node.meanStep
        self.medianStep = node.medianStep
        self.before = node.before
        self.after = node.after
        self.parent = node.parent
        self.position = pos

    @staticmethod
    def createGraph(nodeVal):
        """Create graph from given node"""
        pass

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class RawNode."""
        return {
            "node_id": self.nid,
            "event_attribute": self.value,
            "Pattern": self.pattern,
            "value": self.seqCount,
            "median_index": self.medianStep,
            "average_index": self.meanStep,
            "position": self.position
        }

    @staticmethod
    def jsonSerializeDump(obj):
        """static method to call jsonDefaultDump on all custom objects"""
        if hasattr(obj, "jsonDefaultDump"):
            print("default dump")
            return obj.jsonDefaultDump()

        return None  # obj.__dict__

    def printNode(self):
        """ Prints details for a node."""
        print(f'node {self.nid}, value {self.value}, Pattern {self.pattern}, \
        meanStep {self.meanStep} seqcount {self.seqCount} pos {self.position}')

    @staticmethod
    def printNodes(nodeList):
        """Print all nodes in the list."""
        for node in nodeList:
            node.printNode()


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


    def collapseNode(self):
        """Gets rid of extra nrange(lenodes and links"""
        RawNode.printNodes(self.nodes)
        delNodes = []
        delLinks = []
        newLinks = []

        for node in self.nodes:
            if node.value == -2:
                # ideally. there should be one source
                linkArrSrc = [
                    x for x in self.links if x.target == node.nid]
                print(f'source1 {[lnk.source for lnk in linkArrSrc]}')
                print(f'target1 {[lnk.target for lnk in linkArrSrc]}')
                # if len(linkArrSrc) == 1:
                #    linkArrSrc = linkArrSrc[0]

                linkArrTrgt = [
                    x for x in self.links if x.source == node.nid]
                print(f'source2 {[lnk.source for lnk in linkArrTrgt]}')
                print(f'target2 {[lnk.target for lnk in linkArrTrgt]}')

                if len(linkArrSrc) > 1 and len(linkArrTrgt) > 1:
                    print(
                        f'len source {len(linkArrSrc)}, len target {len(linkArrTrgt)}')
                    # continue
                    # [x.printNode() for x in self.nodes if x.node_id in ]
                    raise ValueError('multiple source and target')

                for j, _ in enumerate(linkArrSrc):
                    for i, _ in enumerate(linkArrTrgt):
                        newLinks.append(
                            Links(linkArrSrc[j].source,
                                  linkArrTrgt[i].target, linkArrTrgt[i].count))
                        delLinks.append(linkArrTrgt[i])
                    delLinks.append(linkArrSrc[j])

                delNodes.append(node)

        #print(f'Node delete {[node. nid for node in delNodes]}')
        # print(
        #    f'Link delete {[((link.source, link.target)) for link in delLinks]}')

        # print(self.printGraph())

        delNodeIndices = [self.nodes.index(x) for x in delNodes]
        delLinkIndices = [self.links.index(x) for x in delLinks]

        #print(f'Node delete {delNodeIndices}')
        #print(f'Link delete {delLinkIndices}')
        print(delLinkIndices)
        for idx in sorted(delNodeIndices, reverse=True):
            del self.nodes[idx]

        # To sure uniqueness we use list(set) operation here
        for idx in sorted(list(set(delLinkIndices)), reverse=True):
            print(f'index {idx}')
            del self.links[idx]

        self.links.extend(newLinks)

    def leftMost(self, node):
        current = node
        
        while(current):
            if current.before:
                break
            print(f'current {current}')
            current = current.before

        return current

    def findSuccessor(self, rootNode, node):

        if node.after:
                return [self.leftMost(node.after[i]) for i in range(len(node.after))]
        successor = node.parent
        while(successor):
            if successor not in node.after:
                break
            node = successor
            successor = node.parent
        return successor

    def allignNodes(self):
        """ Align  nodes according to their position in sequence. """
        """ rootNode = self.nodes[0]
        for node in self.nodes:
            successor = self.findSuccessor(rootNode, node)
            print(f'nodes {[node.nid]} successor {successor}')
            print(successor)
            linkExists = [x for x in self.links if x.source ==
                          node.nid and x.target == successor.nid]

            if not linkExists:
                self.links.append(Links(node.nid, successor.nid, 0)) """

        print("nodes sorted")
        node = sorted(self.nodes, key=lambda x: x.position)
        RawNode.printNodes(node)

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
